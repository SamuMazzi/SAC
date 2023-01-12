from api import get_cars
from flask import Flask, render_template, request
from google.cloud import firestore
from wtforms import Form, BooleanField, FloatField, TextAreaField, SubmitField

class Myform(Form):
    make = TextAreaField('marca')
    cc = FloatField('potenza')
    price = FloatField('price')
    used = BooleanField('Used')
    submit = SubmitField('Submit')

app = Flask(__name__)

db = firestore.Client("es13marzosm")

# Create object to encapsulate model (for form)
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def filter_req(filters: Myform):
    collect = db.collection('cars')
    for one_filter in filters.data:
        if one_filter == 'submit':
            continue
        print(one_filter)
        print(filters[one_filter].data)
        if filters[one_filter].data:
            print('in for ' + one_filter)
            collect = collect.where(one_filter, '==', filters[one_filter].data)
    out = []
    for key in collect.stream():
        print(key.to_dict())
        out.append(key.to_dict())
    return out

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        cform = Myform(request.form)
        cars = filter_req(cform)
    
    if request.method=='GET':
        cform=Myform() #obj=Struct(**cform)
        cars = get_cars()
    
    return render_template('index.html', cars=cars, form=cform, make=cform['make'], cc=cform['cc'], price=cform['price'], used=cform['used'])

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
