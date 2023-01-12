import uuid
from flask import Flask, request
from google.cloud import firestore
from flask import Flask, request
from flask_restful import Resource, Api

poss_engines = ['diesel', 'petrol', 'hybrid', 'electric']
keys = ['make', 'model', 'cc', 'cv', 'price', 'used']

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
cars_collection = db.collection('cars')

def get_cars():
    list_cars = cars_collection.stream()
    out = []
    for car in list_cars:
        out.append(car.to_dict())
    return out
    
def get_car(car_id: str):
    return cars_collection.document(car_id).get().to_dict()

def add_car(car_id: str, data_car: dict):
    print(db._client_info.__dict__)
    if get_car(car_id) is not None:
        return False
    cars_collection.document(car_id).set(data_car)
    return True

def add_car_user(data_user, data_car):
    db.collection('users').document(data_user['email']).set(data_user)
    data_car['user'] = data_user['email']
    id = uuid.uuid4()
    add_car(id, data_car)
    

def check_obj(obj_car):
    if type(obj_car['make']) is not str or len(obj_car['make']) < 3:
        raise Exception('1')
    if type(obj_car['model']) is not str or len(obj_car['model']) < 3:
        raise Exception('2')
    if type(obj_car['cc']) is not int or type(obj_car['cv']) is not int or obj_car['cv'] < 59:
        raise Exception('3')
    if type(float(obj_car['price'])) is not float:
        raise Exception('4')
    if type(obj_car['used']) is not bool:
        raise Exception('5')
    real_obj = {key: obj_car[key] for key in keys}
    return real_obj

class CleanResource(Resource):
    def get(self):
        try:
            delete_collection(db.collection('/'), 10)
            return None, 200
        except:
            return None, 400

class CarResource(Resource):
    def get(self, car_id):
        try:
            uuid.UUID(car_id)
            return get_car(car_id), 200
        except:
            return None, 404

    
    def post(self, car_id):
        try:
            uuid.UUID(car_id)
            data_json = check_obj(request.json)
            if not add_car(car_id, data_json):
                return None, 409
            return data_json, 201
        except Exception as e:
            print(e)
            return None, 400

class SellResource(Resource):
    keys_user = ['nome', 'cognome', 'email']
    def test_data_user(self, data_user):
        for key in SellResource.keys_user:
            if data_user[key] is not str:
                raise Exception()
        if '@' not in data_user['email']:
            raise Exception()
    def post(self, car_id):
        try:
            data_user = self.test_data_user({key: request.json[key] for key in SellResource.keys_user})
            data_json = check_obj(request.json)
            if not add_car_user(data_user, data_json):
                return None, 409
            return data_json, 201
        except:
            return None, 400

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1/car'
api.add_resource(CleanResource, f'{basePath}/clean')
api.add_resource(CarResource, f'{basePath}/<string:car_id>')
api.add_resource(SellResource, f'{basePath}/sell/<string:car_id>')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
