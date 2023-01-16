from datetime import datetime

keys = ['make', 'model', 'cc', 'cv', 'price', 'used']
obj = {
        'plant': {
            'name': 'Bonsai',
            'sprout-time': "3 months",
            'full-growth': "2 years",
            'edible': False
        },
        'num': 3
}

def check_obj(obj_in):
    if type(obj_in['num']) is not int or obj_in['num'] < 1:
        raise Exception()
    plant_dict = obj_in['plant']
    if type(plant_dict['name']) is not str or len(plant_dict['name']) < 5:
        raise Exception()
    if type(plant_dict['sprout-time']) is not str or len(plant_dict['sprout-time']) < 5:
        raise Exception()
    if type(plant_dict['full-growth']) is not str or len(plant_dict['full-growth']) < 5:
        raise Exception()
    if type(plant_dict['edible']) is not bool:
        raise Exception()
    # real_obj = {key: obj_in[key] for key in keys}
    return obj_in

def check_date(date):
    """Raise exception if something is wrong"""
    datetime.strptime(date, '%Y-%m-%d').date()

def check_plant_path(plant):
    if type(plant) is not str or len(plant) < 3 or len(plant) > 20:
        raise Exception()
    
def check_path_param(plant, date):
    check_plant_path(plant)
    check_date(date)