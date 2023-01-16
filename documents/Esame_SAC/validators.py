from datetime import datetime

keys = ['make', 'model', 'cc', 'cv', 'price', 'used']

def check_obj(obj_in):
    if type(obj_in['make']) is not str or len(obj_in['make']) < 3:
        raise Exception()
    if type(obj_in['model']) is not str or len(obj_in['model']) < 3:
        raise Exception()
    if type(obj_in['cc']) is not int or type(obj_in['cv']) is not int or obj_in['cv'] < 59:
        raise Exception()
    if type(obj_in['price']) is not float:
        raise Exception()
    if type(obj_in['used']) is not bool:
        raise Exception()
    real_obj = {key: obj_in[key] for key in keys}
    return real_obj


def check_date(date):
    """Raise exception if something is wrong"""
    datetime.strptime(date, '%Y-%m-%d').date()