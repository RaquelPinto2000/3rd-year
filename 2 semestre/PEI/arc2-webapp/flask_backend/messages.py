import sys
import paho.mqtt.client as mqtt
from datetime import datetime
from flask import Flask
import json

#import stuff from influxdb
from influxdb import InfluxDBClient

#setup database
db_client = InfluxDBClient('localhost', 8086, 'admin', 'Password1', 'mydb2')
db_client.create_database('mydb2')
db_client.get_list_database()
db_client.switch_database('mydb2')


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('#')

def on_publish(client,userdata,result): #create function for callback
    #print("data published \n")
    #print(userdata,result)
    pass

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    #res = '%s %s'%(topic,payload)
    res = json.loads(payload)
    #print(res)
    #Setup db payload

    #{'long': -8.657433655117947, 'lat': 40.64120637331829, 'speed': 7.2, 'heading': 33.806999999999995, 'length': 2.6, 'car_id': 24, 'Timestamp': 1618243854.974041, 'class': 3}
    #{'long': -8.65765085344354, 'lat': 40.641432652327765, 'speed': 9.4, 'heading': 35.223, 'length': 4.6000000000000005, 'car_id': 22, 'Timestamp': 1618243854.976857, 'class': 1}
    #{'longitude': -8.6409624, 'RSSI': -71, 'Timestamp': 1618243855.039855, 'speed': 3.5, 'heading': 56.2, 'OBU_ID': '86', 'class': 6, 'latitude': 40.6439821, 'altitude': 12.7}
    #{'longitude': -8.6409624, 'RSSI': -71, 'Timestamp': 1618243855.039855, 'speed': 3.5, 'heading': 56.2, 'OBU_ID': '86', 'class': 6, 'latitude': 40.6439821, 'altitude': 12.7}
    #{'Timestamp': 1618243854.0, 'n_cars': '1', 'speed': '2.6000000000000005'}
    #print(res)

    if 'class' in res:
        #print("1")
        if 'OBU_ID' in res:
           # print("2")
            if res['class'] == 10 or res['class'] == 5: #Special Vehicle or Passenger Car
                #print(res)
                json_payload = []
                
                data = {
                    "measurement": "coordinates",
                    "tags": {
                        "car_id": res['OBU_ID'],
                        "car_class": res['class']
                    },
                    "time": datetime.now(),
                    "fields":{
                        'latitude': res['latitude'],
                        'longitude': res['longitude']
                    }
                }
                #print(data)
                # DELETE FROM "coordinates" WHERE "car_id" = '28'     <--- para dar delete
                # select * FROM "coordinates" WHERE "car_id" = '27'   <--- selecionar o que queremos
                result = db_client.query("SELECT * FROM coordinates")
                #print(result)

                #str(res['car_id'])
                #print(str(res['car_id']))
                db_client.query("DELETE FROM coordinates WHERE car_class = '"+str(res['OBU_ID'])+"'" ) #

                ola = list(result.get_points(tags={'car_id': str(res['OBU_ID'])}))
                print(ola)
                json_payload.append(data)       # adiciona novos dados ao json

                #send payload
                db_client.write_points(json_payload)     # adiciona a base de dados
            



    #with open(f_name,'a+') as f_out:
    #    f_out.write("%s\n"%res)

broker_ip = '10.0.20.32'
port = 1884
now = datetime.now()
f_name = 'samples/mixed/full_sample_%s.txt' % now.strftime("%d_%m_%Y_%H_%M")

if len(sys.argv) > 1:
    f_name = sys.argv[1]
    if len(sys.argv) > 2:
        broker_ip = sys.argv[2]
        if len(sys.argv) > 3:
            port = int(sys.argv[3])


#Connects to the broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
print('[%s] Publishing messages from ´%s´ into broker hosted at %s:%d' % (now.strftime("%d/%m/%Y %H:%M"),f_name,broker_ip,port))
try: 
    client.connect(broker_ip, port)
except:
    print('ERROR: Could not connect to broker %s:%d' % (broker_ip,port))



client.loop_forever()

