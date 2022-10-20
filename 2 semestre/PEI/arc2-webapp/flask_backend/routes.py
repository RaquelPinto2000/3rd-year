# flask
import re
import os
from flask import request, jsonify, render_template, flash, redirect, send_from_directory, Response
from flask_login import login_user, login_required, logout_user, current_user
from flask_backend import app, db, socketio  # app and database
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_backend import camera
from flask_socketio import SocketIO, emit, send
import geopy.distance

# database objects and queries
from flask_backend.database.db_schemas import accident_schema, accidents_schema
from flask_backend.database.db_models import Accident, Car
from flask_backend.database.queries import *
from flask_backend.erros import *
from datetime import datetime
from time import time
import json
import requests

#from flask_backend.messages import messages

# import stuff from influxdb
from influxdb import InfluxDBClient, client

# data processing
from flask_backend.data_processing import get_location_address, severity_calc, check_burn
import random

# media
from flask_backend.media_processing import init_media, convert_avi_to_mp4, rmMedia

# setup database
db_client = InfluxDBClient('localhost', 8086, 'admin', 'Password1', 'mydb2')
db_client.create_database('mydb2')
db_client.get_list_database()
db_client.switch_database('mydb2')

# video adding

ALLOWED_EXTENSIONS = set(['avi', 'mp4'])


@app.route('/login/request', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['passwd']
    print(email)
    print(password)
    user = get_user_by(email=email)
    if can_login(email, password, user):
        login_user(can_login(email, password, user))
        user.last_login = f"{datetime.now():%Y-%m-%d %H:%M}"
        print(user_schema.dump(user))
        add_user_to_database(user)
        return jsonify({"response": "Done"})
    else:
        return jsonify({"error": "Invalid username or password"})


@app.route('/#admin')
@login_required
def web():
    return render_template("index.html")


@app.route('/')
def index():

    return render_template("index.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "you are logged out"


@app.route('/home')
@login_required
def home():
    return user_schema.dump(current_user)


# Add video
@app.route('/add_video', methods=['POST'])
def add_video():

    if "file" not in request.files:
        return jsonify(no_file)

    if "id" not in request.values:
        return jsonify(no_id_video)

    file = request.files['file']  # retira o file do request
    video_id = request.values["id"]  # retira o video_id para pesquisa
    type = file.filename.split(".")[1]

    if type not in ALLOWED_EXTENSIONS:
        return jsonify(video_type_not_allowed)

    # devolve accident que contem o video_id
    accident = get_accident_by(video_id, filter="video_id")

    if not accident:
        return jsonify(no_accident)

    accident_id = str(accident.id)  # get id do accident
    video_number = str(accident.video_total + 1)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], accident_id +
                             "/video/" + video_number + "." + type)  # create path for file
    file.save(file_path)  # save temporary file on directory

    if type == "avi":
        convert_avi_to_mp4(os.path.join(
            app.config['UPLOAD_FOLDER'], accident_id+"/video/" + video_number))  # convert file to a mp4

    return add_video_to_database(video_id)  # add path of file to database

# Create a Accident


@app.route('/add_accident', methods=['POST'])
def add_accident():
    
    location = request.json['location']
    # print("LOCATION",location,"\n\n")
    
    video_id = int(request.json['video_id'])
    
    accident = get_accident_by(location, filter="belongs")
    
    congested = get_accident_by(location, filter="congested")

    if not accident:
        location["address"], city = get_location_address(
            location["lat"], location["lng"])
        accident = Accident(location, city, video_id)
    
    if (congested >= 2):
        print("This accident is in a congested area.\n")
        accident.congested = 1
    else:
        print("This accident is not in a congested area.\n")
        accident.congested = 0
    
    accident.n_cars_involved += 1
    n_people = request.json["n_people"]
    accident.n_people += request.json["n_people"]

    velocity = request.json["velocity"]
    ABS = request.json["ABS"]
    temperature = request.json["temperature"]
    airbag = True  # request.json["airbag"]
    overturned = request.json["overturned"]
    hazard_ligths = request.json["hazard_lights"]
    num_seatbelts = request.json["all_seatbelts"]

    fire_check = check_burn(temperature)

    if fire_check:
        accident.fire = 1
    else:
        accident.fire = 0

    severity = severity_calc(n_people, velocity, ABS,
                             airbag, overturned, num_seatbelts, fire_check)

    if accident.n_cars_involved > 1:
        accident.damage = (((accident.damage) * (accident.n_cars_involved - 1)
                            ) + severity) / accident.n_cars_involved
    else:
        accident.damage = severity

    car = Car(velocity, n_people, temperature, airbag,
              ABS, hazard_ligths, overturned, severity)
    

    add_accident_to_database(accident, car)
    init_media(accident.id, (location["lat"], location["lng"]))
    

    cameras = checkNearbyCameras((location["lat"], location["lng"]))
    addCamerasToAccident(cameras, accident.id)
    print(cameras)
    """
    for c in cameras:
        print(c)
        global idRtsp
        idRtsp[str(c['id'])] = c['link']
        socketio.emit('rtsp', {'accidented_car_id': str(accident.id), 'carID': str(c['id']), 'rtspLink': c['link']})
    """
    
    return accident_schema.jsonify(accident)


@app.route('/add_user', methods=['POST'])
def add_user():
    email = request.json['email']
    role = int(request.json['role'])
    role_type = request.json['role_type']
    city = request.json['city']
    user = User(email, role, role_type, city)
    if add_user_to_database(user):
        return jsonify({"response": "Done"})


@app.route('/delete_user/<mail>', methods=['POST'])
def delete_user(mail):
    delete_user_from_database(mail)
    if not get_user_by(email=mail):
        return jsonify(
            {"succes": True}
        )
    return jsonify(
        {"succes": False}
    )
#i = 0


@app.route('/markers/<id>', methods=['POST'])
def get_amb_id(id):     # recebe o id da ambulancia do site

    ambulance_id = request.json['ambulance']
    print(str(ambulance_id)+"recebi acidente")

    accident = get_accident_by(id, filter="id_only_accident")
    print(accident)
    accident.ambulance = ambulance_id

    db.session.commit()

    return "watzare"


# 40.63479360609901, -8.654912771434054 coordenadas hospital de aveiro
@app.route('/markers/<id>', methods=['GET'])
def get_Markers(id):  # localizacao da ambulancia
    # falta trocar o '21' pelo id da ambulancia que queremos

    accidentdb = get_accident_by(id, filter="id_only_accident")

    getAmbu = db_client.query(
        "SELECT * FROM coordinates WHERE car_id = '"+str(accidentdb.ambulance)+"'")

    ambData = list(getAmbu.get_points(
        tags={'car_id': str(accidentdb.ambulance)}))

    if len(ambData) == 0:
        latitudee = 40.63479360609901
        longitudee = -8.654912771434054
    else:
        latitudee = ambData[0]['latitude']
        longitudee = ambData[0]['longitude']

    #global i
    # i+=0.0001

    return jsonify(
        {"lat": latitudee, "lng": longitudee}
    )


@app.route('/CarsMarkers/<id>', methods=['GET'])
def get_CarsMarkers(id):

    #accidentdb = get_accident_by(id, filter="id_only_accident")

    #getAmbu = db_client.query("SELECT * FROM coordinates WHERE car_id = '"+str(accidentdb.ambulance)+"'")
    getAllCars = db_client.query(
        "SELECT * FROM coordinates WHERE car_class = '"+str(5)+"'")

    #ambData = list(getAmbu.get_points(tags={'car_id': str(accidentdb.ambulance)}))
    carData = list(getAllCars.get_points(tags={'car_class': str(5)}))
    # print(carData)
    """
    if len(ambData) == 0:
        latitudee = 40.63479360609901
        longitudee = -8.654912771434054 
    else:
        latitudee = ambData[0]['latitude']
        longitudee = ambData[0]['longitude']
    """

    return jsonify(
        {'carData': carData}
    )

@app.route('/CameraMarkers/<id>', methods=['GET'])
def get_CameraMarkers(id):

    cameras = get_all_cameras()
    print(cameras)
    

    return jsonify(
        {'camData': cameras}
    )


@app.route('/register_user', methods=['POST'])
def register_user():

    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    user = get_user_by(email)
    if register_user_to_database(username, email, password=generate_password_hash(password, method='sha256')):
        login_user(can_login(email, password, user))
        user = get_user_by(email=email)
        user.last_login = f"{datetime.now():%Y-%m-%d %H:%M}"
        print(user_schema.dump(user))
        add_user_to_database(user)
        return jsonify({"response": "Done"})
    else:
        return jsonify({"error": "Invalid user or email. Please contact the Administrator"})


@app.route('/all_users', methods=['GET'])
def get_users():
    return get_all_users()


@app.route('/update_user', methods=['POST'])
def update_user():
    user = get_user_by(email=request.json["last_email"])
    print(request.json)
    if "Username" in request.json:
        user.Username = request.json["Username"]
    if "password" in request.json:
        user.password = request.json["password"]
    if "first_name" in request.json:
        user.first_name = request.json["first_name"]
    if "last_name" in request.json:
        user.last_name = request.json["last_name"]
   # if "birth_date" in request.json:
    #    user.birth_date = request.json["birth_date"]
    if "address" in request.json:
        user.address = request.json["address"]
    if "city" in request.json:
        user.city = request.json["city"]
    if "country" in request.json:
        user.country = request.json["country"]
    if "postal_code" in request.json:
        user.postal_code = request.json["postal_code"]
    if "telephone" in request.json:
        user.telephone = request.json["telephone"]
    if "work_institution" in request.json:
        user.work_institution = request.json["work_institution"]
    if "profession" in request.json:
        user.profession = request.json["profession"]
    if "about" in request.json:
        user.about = request.json["about"]
    if "role" in request.json:
        user.role = request.json["role"]
    if "role_type" in request.json:
        user.role_type = request.json["role_type"]
    if "email" in request.json:
        user.email = request.json["email"]

    print(user_schema.dump(user))
    add_user_to_database(user)
    return jsonify(
        {"succes": True}
    )


@app.route('/delete_accident/<id>', methods=['POST'])
def delete_accident(id):
    print("delete accident:"+id)
    delete_accident_from_database(id)
    rmMedia(id)
    return jsonify(
        {"succes": True}
    )

# See Accident


@app.route('/accident/<id>', methods=['GET'])
def get_accident(id):
    return get_accident_by(id, filter="id")


@app.route('/accident_status/<id>', methods=['GET'])
def get_accident_status(id):
    return jsonify(get_accident_by(id, filter="id_only_accident").status)


@app.route('/set_accident_status/<id>', methods=['POST'])
def set_accident_status(id):
    status = int(request.json['status'])
    return change_accident_status(id, status)


@app.route('/set_accident_injured/<id>', methods=['POST'])
def set_accident_injured(id):
    status = int(request.json['injured'])
    print(status)
    return change_accident_injured(id, status)


@app.route('/accident_icon/<status>', methods=['GET'])
def get_accident_icon(status):
    print(status)
    if (int(status) == 1):
        return send_from_directory(app.config['UPLOAD_FOLDER'], "icon_map_yellow.png", as_attachment=True)
    if(int(status) == 2):
        return send_from_directory(app.config['UPLOAD_FOLDER'], "icon_map_green.png", as_attachment=True)
    if (int(status) == 3):
        return send_from_directory(app.config['UPLOAD_FOLDER'], "ambulancia.png", as_attachment=True)
    if (int(status) == 4):
        return send_from_directory(app.config['UPLOAD_FOLDER'], "icon_map_grey.png", as_attachment=True)
    if (int(status) == 5):
        return send_from_directory(app.config['UPLOAD_FOLDER'], "icon_map_passenger_car.png", as_attachment=True)
    if (int(status) == 6):
        return send_from_directory(app.config['UPLOAD_FOLDER'], "icon_map_camera.png", as_attachment=True)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'], "icon_map_red.png", as_attachment=True)

# See All Accident


@app.route('/list_accidents', methods=['GET'])
def get_accidents():
    if int(current_user.role) == 0:
        return get_accident_by(None, filter="all")
    else:
        return get_accident_by(None, filter="all", city=current_user.city)

@app.route('/list_ambulances', methods =['GET'])
def get_ambulances():
    result = db_client.query("SELECT * FROM coordinates  WHERE car_class='10'")
    resulte = list(result.get_points(tags={'car_class': '10'}))   # gives ambulas

    return jsonify(resulte)

# Available filters:
# default = between -> show accidents by date
# cars,people,injured,severity,status
# usage "range_accidents?id=x&filter=X"
#


@app.route('/range_accidents', methods=['GET'])
def get_range_accidents():
    id = request.args.get('id', 1, type=int)
    filter = request.args.get('filter', "between", type=str)
    quantity = request.args.get('quantity', "All", type=str)
    order = request.args.get('order', "Ascending", type=str)
    if int(current_user.role) == 0:
        return get_accident_by(((id - 1) * 10, id * 10), filter=filter, quantity=quantity, order=order)
    else:
        return get_accident_by(((id - 1) * 10, id * 10), filter=filter, quantity=quantity, order=order, city=current_user.city)


@app.route('/num_accidents', methods=['GET'])
def get_number_accidents():
    quantity = request.args.get('quantity', "All", type=str)
    if int(current_user.role) == 0:
        return str(get_num_accidents(quantity))
    else:
        return str(get_num_accidents(quantity, city=current_user.city))

# accident media


@app.route('/media/<path:path_to_file>', methods=['GET'])
def get_media_photos_id(path_to_file):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=path_to_file, as_attachment=True)


@app.route('/Nmedia/<path:path_to_file>')
def get_num_photos(path_to_file):
    txt_or_csv = [f for f in os.listdir(os.path.join(
        app.config['UPLOAD_FOLDER'], path_to_file)) if re.search(r'.*\.(jpeg)$', f)]
    return str(len(txt_or_csv))


@app.route('/congested_car/<id>', methods=['GET'])
def congestedCar(id):
    loc = get_accident_by(id, filter="id")
    # print(loc["location"])

    #result = get_accident_by(loc, filter="congested")
    # print(result)

    return loc


idRtsp = {}


@app.route('/addRTSP', methods=['POST'])
def accident():

    car = get_car(request.json['accidented_car_id'])
    res = car_schemas.dump(car)

    print(request.json['gateway'])
    print(type(request.json['gateway']))
    if request.json['gateway']:

        json_body = [
            {
                "measurement": "livestream",
                "tags": {
                    "car_id": request.json['my_id'],
                    "acc_id": res[0]['accident_id'],
                    "car_class": request.json['car_class']
                },
                "time": datetime.now(),
                "fields": {
                    "link_RTSP": request.json['rtsp'],
                    "stream_started": '1'
                }
            }
        ]

        print("Starting Livestream for id: " + str(json_body[0]['tags']['car_id']) + "\nlink: " + json_body[0]['fields']['link_RTSP'])
        socketio.emit('rtsp', {'accidented_car_id': str(json_body[0]['tags']['acc_id']), 'carID': str(json_body[0]['tags']['car_id']), 'rtspLink': str(json_body[0]['fields']['link_RTSP'])})
    else:
        json_body = [
            {
                "measurement": "livestream",
                "tags": {
                    "car_id": request.json['my_id'],
                    "acc_id": res[0]['accident_id'],
                    "car_class": request.json['car_class']
                },
                "time": datetime.now(),
                "fields": {
                    "link_RTSP": request.json['rtsp'],
                    "stream_started": '0'
                }
            }
        ]

    db_client.write_points(json_body)
    return jsonify(json_body)


@app.route('/startStream/<id_acc>/<id_target>', methods=['GET'])
def startStream(id_acc, id_target):

    result = db_client.query("SELECT * FROM livestream WHERE car_id='" + str(id_target) + "'")
    rtsplink = list(result.get_points(tags={'car_id': str(id_target)}))[0]['link_RTSP']
    #print(rtsplink)
    #print(type(rtsplink))
    print("Starting Livestream for id: " + str(id_target) + "\nlink: " + rtsplink)

    socketio.emit('rtsp', {'accidented_car_id': str(id_acc), 'carID': str(id_target), 'rtspLink': rtsplink})
    
    db_client.query("DELETE FROM livestream WHERE car_id='" + str(id_target) + "'")

    json_body = [
        {
            "measurement": "livestream",
            "tags": {
                "car_id": id_target,
                "acc_id": id_acc,
                "car_class": list(result.get_points(tags={'car_id': str(id_target)}))[0]['car_class']
            },
            "time": datetime.now(),
            "fields": {
                "link_RTSP": rtsplink,
                "stream_started": '1'
            }
        }
    ]
    db_client.write_points(json_body)

    return jsonify({str(id_target): rtsplink})


@app.route('/stopStream/<accident_id>/<car_id>', methods=['POST'])
def stopStream(accident_id, car_id):
    """
    socketio.emit('stop', {'id': accident_id,
                  'car_id': car_id, 'url': request.json['url']})
    """
    port = str(9000 + int(car_id))
    print(port)
    socketio.emit('stop', {'port': port})
    db_client.query("DELETE FROM livestream WHERE car_id='" + str(car_id) + "'")

    #return {'id': accident_id, 'car_id': car_id, 'url': request.json['url']}
    return {'port': port}


lives = {}


@app.route('/videos/<id>', methods=['GET'])
def get_videos(id):
    # Example of expected struture to be returned by this function
    # a = {id: [{"port": "ws://localhost:9002"}, {"port": "ws://localhost:9003"}, {"port": "ws://localhost:9004"}]}

    result = db_client.query("SELECT * FROM livestream WHERE acc_id='" + str(id) + "'")
    lives = list(result.get_points())
    
    response = {int(id):[]}
    
    for live in lives:
        if live['stream_started'] == '1':
            response[int(id)].append({"port": "ws://steamcity02.nap.av.it.pt:" + str(int(live['car_id']) + 9000)})

    return response




@socketio.on('response2')
def test_message(msg1, msg2):
    global lives
    lives[msg1] = msg2


"""
@socketio.on('response')
def test_message2(msg1):
    global lives
    lives[msg1] = msg2
    print('received message: ' + str(lives))
"""


@socketio.on('message')
def test_message(msg):
    print('received message: ' + msg)


@socketio.on('connect')
def connect():
    print("Got a connection...\nTesting it by sending 1 message")
    emit('teste', {'data': 'If you see this the test was successful'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

# Create a Accident DENM


@app.route('/add_accident_denm', methods=['POST'])
def add_accident_denm():
    location = request.json['location']
    video_id = int(request.json['video_id'])

    #accident = get_accident_by(location, filter="belongs")

    # if not accident:
    location["address"], city = get_location_address(
        location["lat"], location["lng"])
    accident = Accident(location, city, video_id)

    accident.n_cars_involved += 1
    n_people = request.json["n_people"]
    accident.n_people += request.json["n_people"]

    velocity = 100  # request.json["velocity"]
    ABS = True  # request.json["ABS"]
    temperature = request.json["temperature"]
    airbag = 0  # request.json["airbag"]
    overturned = True  # request.json["overturned"]
    hazard_ligths = True  # request.json["hazard_lights"]
    num_seatbelts = True  # request.json["all_seatbelts"]

    fire = True  # check_burn(temperature)

    severity = severity_calc(n_people, velocity, ABS,
                             airbag, overturned, num_seatbelts, fire)

    if accident.n_cars_involved > 1:
        accident.damage = (((accident.damage) * (accident.n_cars_involved - 1)
                            ) + severity) / accident.n_cars_involved
    else:
        accident.damage = severity

    car = Car(velocity, n_people, temperature, airbag,
              ABS, hazard_ligths, overturned, severity)

    add_accident_to_database(accident, car)
    init_media(accident.id, (location["lat"], location["lng"]))

    cameras = checkNearbyCameras((location["lat"], location["lng"]))
    addCamerasToAccident(cameras, accident.id)
    print(cameras)

    return accident_schema.jsonify(accident)




def checkNearbyCameras(accCoords):
    cameras = get_all_cameras()
    validCameras = []
    print(cameras)
    for c in cameras:
        coordsC = (c['latitude'],c['longitude'])
        dist = geopy.distance.distance(coordsC, accCoords).m
        if dist <= 50:
            validCameras.append({'id': c['id'], 'link': c['linkRTSP']})

    return validCameras

def addCamerasToAccident(cameras, accident_id):
    for cam in cameras:
        json_body = [
            {
                "measurement": "livestream",
                "tags": {
                    "car_id": cam['id'],
                    "acc_id": accident_id,
                    "car_class": '0'
                },
                "time": datetime.now(),
                "fields": {
                    "link_RTSP": cam['link'],
                    "stream_started": '0'
                }
            }
        ]

        db_client.write_points(json_body)
        startStream(accident_id, cam['id'])

@app.route('/ambulances_by_user', methods=['GET'])
def get_ambulances_by_user():
    # lista onde vou guardar as ambulancias deste user
    current_user_ambulances = []
    # current_user.id   devolve o id de quem está logado
    current_id = current_user.id
    # todas as ambulancias
    all = get_all_ambulances_by_user()
    # filtrar so os do user logado
    for i in all:
        if i['id_user'] == current_id:
            current_user_ambulances.append(i['id_ambulance'])         

    return jsonify(current_user_ambulances)