#!/usr/bin/python3

from datetime import datetime
from typing import List
from validators import check_obj, check_date
from utilities import delete_collection, date_from_str
from flask import Flask, request
from google.cloud import firestore
from flask_restful import Resource, Api

db = firestore.Client()
name_collection = 'letture'
consumi_collection = db.collection(name_collection)
costo = 0.5

def get_last_consumi(n: int, date: datetime):
    dates: List[datetime] = []
    values = []
    docs = consumi_collection.where('date', '<', date.timestamp()).order_by('date', direction=firestore.Query.DESCENDING).limit(n).stream()
    for doc in docs:
        my_date = datetime.fromtimestamp(doc.get('date'))
        dates.append(my_date)
        values.append(doc.get('value'))
    dates.reverse()
    values.reverse()
    return dates, values


def interpol(new_date: datetime):
    dates, values = get_last_consumi(2, new_date)
    if len(dates) == 0:
        return 0
    elif len(dates) == 1:
        return values[0]
    diff1 = (dates[1] - dates[0]).total_seconds()
    diff2 = (new_date - dates[1]).total_seconds()
    c = values[1] + ((values[1] - values[0])/diff1)*diff2
    return c

def get_consumo(data: str):
    return consumi_collection.document(data).get().to_dict()

def add_consumo(date: str, obj_in: dict):
    if get_consumo(date) is not None:
        return False
    
    consumi_collection.document(date).set({
        'value': obj_in['value'],
        'date': date_from_str(date).timestamp()
    })
    return True


class CleanResource(Resource):
    def get(self):
        try:
            delete_collection(db.collection(name_collection))
            return None, 200
        except:
            return None, 400

class ObjResource(Resource):
    def get(self, data):
        try:
            check_date(data)
            consumo = get_consumo(data)
            if consumo is None:
                return {
                    'value': interpol(date_from_str(data)),
                    'isInterpolated': True
                }, 200
            else:
                return {
                    'value': consumo['value'],
                    'isInterpolated': False
                }, 200
        except Exception as e:
            print(e)
            return None, 400

    
    def post(self, data):
        try:
            check_date(data)
            data_json = check_obj(request.json)
            if not add_consumo(data, data_json):
                return None, 409
            data_json['isInterpolated'] = False
            return data_json, 201
        except:
            return None, 400

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'
api.add_resource(CleanResource, f'{basePath}/clean')
api.add_resource(ObjResource, f'{basePath}/consumi/<string:data>')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
