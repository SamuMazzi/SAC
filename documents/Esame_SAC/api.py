#!/usr/bin/python3

from validators import check_obj
from utilities import delete_collection
from flask import Flask, request
from google.cloud import firestore
from flask_restful import Resource, Api

db = firestore.Client()
cars_collection = db.collection('cars')

class CleanResource(Resource):
    def get(self):
        try:
            delete_collection(db.collection('/'))
            return None, 200
        except:
            return None, 400

class ObjResource(Resource):
    def get(self, car_id):
        out = {}
        try:
            return out, 200
        except:
            return None, 404

    
    def post(self):
        try:
            data_json = check_obj(request.json)
            if not add_car(car_id, data_json):
                return None, 409
            return data_json, 201
        except:
            return None, 400

class NewResource(Resource):
    def post(self):
        try:
            data_json = check_obj(request.json)
            return data_json, 200
        except:
            return None, 400

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1/car'
api.add_resource(CleanResource, f'{basePath}/clean')
api.add_resource(ObjResource, f'{basePath}/<string:car_id>')
api.add_resource(NewResource, f'{basePath}/sell/<string:car_id>')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
