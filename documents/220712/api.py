import datetime
from flask import Flask, render_template, request
from google.cloud import firestore
from flask import Flask, request
from flask_restful import Resource, Api

# app creation
app = Flask(__name__)

# Api creation
api = Api(app)

basePath = '/api/v1/pool'

cap_max = 14

ks = ['name','type','producer','year','price']

add_ks = ['label', 'quantity', 'minimum']

et_type = ['sparkling', 'white', 'red', 'sweet']

db = firestore.Client()
def delete_collection(coll_ref, batch_size):
    docs = coll_ref.list_documents(page_size=batch_size)
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.get().to_dict()}')
        doc.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

# prenot -> date
def add_pren_if_possible(date, user, time):
    path = ('prenotazioni', date)
    order_lanes = ['4', '5', '3', '6', '2', '7', '1', '8']
    pren = get_prenot(date)
    if pren and pren.get(time):
        pren_time = pren.get(time)
        for lane in order_lanes:
            state_lane = pren_time.get(lane)
            if not state_lane or (state_lane and len(pren_time.get(lane)) < 2):
                pren_time[lane] = firestore.ArrayUnion([user])
                db.document(*path).set(pren)
                return True
    else:
        pren = {}
        pren[time] = {
            order_lanes[0]: [user]
        }
        db.document(*path).set(pren)
        return True
    return False

def get_prenot(date):
    path = ('prenotazioni', date)
    return db.document(*path).get().to_dict()

def add_to_slot_if_empty(slot: int, new_data):
    path = ('slots', str(slot))
    if get_slot(slot) is not None:
        return False

    db.document(*path).set(new_data)
    return True

def get_doc_slot(slot: int):
    path = ('slots', str(slot))
    return db.document(*path)

def get_slot(slot: int):
    return get_doc_slot(slot).get().to_dict()


class CleanResource(Resource):
    def get(self):
        try:
            delete_collection(db.collection('/'), 10)
            return None, 200
        except:
            return None, 400

class PoolResource(Resource):
    def check_obj_pren(self, data_json: dict):
        if data_json.get('lane') is not None:
            raise Exception()
        if data_json['others'] is not dict or data_json['time'] is not str:
            raise Exception()
        others = data_json['others']
        for other_pren in others:
            if other_pren['data'] is not str or other_pren['time'] is not str or other_pren.get('lane') is not None:
                raise Exception()
        # date = datetime.datetime.strptime(date, "")
        date_list = date.split('-')

    def get(self, user, date):
        out = {}
        try:
            data = get_prenot(date)
            if not data:
                return out, 200
            for time in data:
                for lane in data[time]:
                    if user in lane:
                        out[time][lane]: user
            return out, 200
        except:
            return None, 404

    
    def post(self, user, date):
        data = {
            'others': {
                "date": '2021-06-19',
                "time": '10-12'
            },
            'time': "08-10"
        }
        try:
            data_json = request.json  #request.is_json() ? request.get_json()
            self.check_obj_pren(data_json)
            res = add_pren_if_possible(date, user, data_json.get('time'))
            if not res:
                return "No lanes available", 412
            others = data_json.get('others')
            if others:
                for pren in others:
                    if not add_pren_if_possible(pren['date'], user, pren['time']):
                        return "No lanes available", 412
                    
            if not res:
                return None, 409
            return others, 201  # in teoria dovresti aggiungere anche quello fuori da others
        except:
            return None, 400

class StatePoolResource(Resource):
    def get(self, date):
        try:
            data = get_prenot(date)
            return data if data is not None else {}, 200
        except:
            return '', 404


api.add_resource(CleanResource, f'{basePath}/clean')
api.add_resource(PoolResource, f'{basePath}/<string:user>/<string:date>')
api.add_resource(StatePoolResource, f'{basePath}/<string:date>')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
