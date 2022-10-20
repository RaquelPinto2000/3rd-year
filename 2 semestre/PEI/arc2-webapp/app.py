from typing import Tuple
from flask_backend import app, socketio
import os
from flask_socketio import SocketIO

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    str1=ASSETS_DIR+'/server.crt'
    str2=ASSETS_DIR+'/server.key'
    #app.run(ssl_context=(str1,str2),host='steamcity02.nap.av.it.pt', port=5000)
    #app.run(host='steamcity02.nap.av.it.pt', port=5000,debug=True)
    #app.run(host='127.0.0.1', port=5001,debug=True)
    #socketio = SocketIO(app)
    socketio.run(app,host='steamcity02.nap.av.it.pt',port=5000)
    #socketio.run(app)
    #app.run()
