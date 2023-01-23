from datetime import datetime

def check_obj(obj_in):
    if type(obj_in['value']) is not int or obj_in['value'] < 0:
        raise Exception()
    real_obj = {
        'value': obj_in['value']
    }
    return real_obj


def check_date(date):
    """Raise exception if something is wrong"""
    datetime.strptime(date, '%d-%m-%Y').date()