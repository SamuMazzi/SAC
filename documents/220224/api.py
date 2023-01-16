#!/usr/bin/python3

from validators import check_path_param, check_obj, check_plant_path
from utilities import delete_collection
from flask import Flask, request
from google.cloud import firestore
from flask_restful import Resource, Api

db = firestore.Client()
plants_collection = db.collection('plants')

def get_plants():
    out = {}
    for name_plant in plants_collection.list_documents():
        out[name_plant] = get_plant(name_plant)
    return out

def get_plant(plant):
    plants_collection.document(plant).get().to_dict()

def get_plant_info_semina(plant, date):
    tmp_plant = get_plant(plant)
    out = {
        'plant': tmp_plant['plant'],
        'num': tmp_plant['semina'][date]
    }
    return out

def add_plant(plant: str, date: str, plant_info: dict):
    server_plant = get_plant(plant)
    if server_plant is not None and server_plant.get('semina') is not None:
        if server_plant.get('semina').get(date) is not None:
            return False
    plants_collection.document(plant).set({
        'plant': plant_info['plant'],
        'semina': {
            date: plant_info['num']
        }
    }, merge=True)

class CleanResource(Resource):
    def get(self):
        try:
            delete_collection(db.collection('data'))
            return None, 200
        except Exception as e:
            print(e)
            return None, 400

class ObjResource(Resource):
    def get(self, date, plant):
        try:
            check_path_param(plant, date)
            out = get_plant_info_semina(plant, date)
            if not out:
                return None, 404
            return None, 201
        except:
            return None, 404

    
    def post(self, date, plant):
        try:
            check_path_param(plant, date)
            data_json = check_obj(request.json)
            if not add_plant(plant, date, data_json):
                return None, 409
            return None, 201
        except:
            return None, 400

class DetailResource(Resource):
    def get(self, plant):
        try:
            check_plant_path(plant)
            out = get_plant(plant)['plant']
            return out, 200
        except:
            return None, 404

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1/garden'
api.add_resource(CleanResource, f'{basePath}/clean')
api.add_resource(ObjResource, f'{basePath}/plant/<string:date>/<string:plant>')
api.add_resource(DetailResource, f'{basePath}/plant/<string:plant>')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
