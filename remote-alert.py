#!flask/bin/python
import os
from flask import Flask, request
from flask.ext import restful
from database import db_session
from database import init_db
from messages import GCM
#@app.teardown_appcontext
#def shutdown_session(exception=None):
#    db_session.remove()

from device import Device


app = Flask(__name__)
api = restful.Api(app)

@app.route('/')
def hello():
    return 'Android push message OK'
    
class MainView(restful.Resource):
    def get(self):
        return {'get': 'out'}

class Read(restful.Resource):
    def get(self, name ):
        try:
            device = Device.query.filter(Device.name == name).first()
            return {'name': device.name , 'registration' : 'Registered' }        
        except:
            return {'name' : '', 'error' : 'not found' }

class DeviceControl(restful.Resource):    
    def remove(self, registration ):
        dev = Device.query.filter(Device.registration == registration).first()        
        if dev:
            db_session.delete(dev)
            db_session.commit()

    def put(self):        
        name = request.json['name']
        registration = request.json['registration']
        return self.register(name, registration)
    
    def register(self, name, registration ):
        self.remove(registration)

        dev = Device.query.filter(Device.name == name).first()
        if not dev:
           dev = Device( name, registration )
        else:
            dev.registration = registration 

        db_session.add(dev)
        db_session.commit()        
        return {name: 'OK' }
        
    def post(self):                
        name = request.json['name']
        registration = request.json['registration']
        return self.register(name, registration)
        

class Android(restful.Resource):
    def send_msg(self, name, message ):
        dev = Device.query.filter(Device.name == name).first()
        if dev:
            gcm = GCM()
            gcm.send( dev.registration, message )            
            return { 'name' : name , 'error' : 'OK' }
        else:
            return { 'name' : name , 'error' : 'not registered' }

    def put(self, name):
        message = request.json['message']
        return self.send_msg( name, message )
        
    def post(self, name):
        message = request.json['message']
        return self.send_msg( name, message )

#Entry points to insert data
#api.add_resource(Read, '/read/<string:name>')
api.add_resource(DeviceControl, '/device')
api.add_resource(Android, '/post/<string:name>')

api.add_resource(MainView, '/')

if __name__ == "__main__":    
    #from database import engine
    #import database
    #Device.__table__.drop(engine)
    #print 'droped table'    
    #init_db()
    #print 'Recreated'
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

