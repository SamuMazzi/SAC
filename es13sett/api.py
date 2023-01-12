from flask import Flask, render_template, request
from google.cloud import firestore
from flask import Flask, request
from flask_restful import Resource, Api

# app creation
app = Flask(__name__)

# Api creation
api = Api(app)

basePath = '/api/v1'

cap_max = 14

ks = ['name','type','producer','year','price']

add_ks = ['label', 'quantity', 'minimum']

et_type = ['sparkling', 'white', 'red', 'sweet']

db = firestore.Client()

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
    def clean_db():
        for i in range(10):
            doc = get_doc_slot(i)
            doc.delete()

    def get(self):
        try:
            CleanResource.clean_db()
            return None, 200
        except:
            return None, 400

class CantinaResource(Resource):
    def get(self, slot_num):
        try:
            if int(slot_num) < 0 or int(slot_num) > 9:
                raise Exception()
            data = get_slot(slot_num)
            if data is None:
                return None, 404
            return data, 200
        except:
            return None, 404

    def post(self, slot_num):
        try:
            if int(slot_num) < 0 or int(slot_num) > 9:
                raise Exception()
            data_json = request.json
            if data_json['label']['type'] not in ['sparkling', 'white', 'red', 'sweet']:
                raise Exception()
            if data_json['label']['year'] < 1900 or data_json['label']['year'] > 2021:
                raise Exception()
            if data_json['label']['price'] < 0:
                raise Exception()
            if data_json['quantity'] < 6 or data_json['quantity'] > 14:
                raise Exception()
            if data_json['minimum'] < 3 or data_json['minimum'] > 8:
                raise Exception()
            res = add_to_slot_if_empty(int(slot_num), data_json)
            if not res:
                return None, 409
            return data_json['label'], 201
        except Exception as e:
            print(e)
            return None, 400

class LabelResource(Resource):
    def _get_labels():
        out = []
        for i in range(10):
            data = get_slot(i)
            if data is not None:
                out.append(data)
        return out
    def validate_type(self, label_type):
        if not isinstance(label_type, str):
            return False
        if label_type not in et_type:
            return False
        return True

    def get(self, label_type):
        if not self.validate_type(label_type):
            return None, 404
        try:
            out = LabelResource._get_labels()
            return out, 200
        except:
            return None, 404


api.add_resource(CleanResource, f'{basePath}/clean')
api.add_resource(CantinaResource, f'{basePath}/slot/<string:slot_num>')
api.add_resource(LabelResource, f'{basePath}/label/<string:label_type>')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
