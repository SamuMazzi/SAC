import requests

mockPayload = {
    "label": {
        "name": "Rote",
        "type": "red",
        "year": 1937,
        "price": 54
    },
    "quantity": 0,
    "minimum": 5
}

base_url = "http://127.0.0.1:8080/api/v1"
headers = {'Content-type': 'application/json'} #, 'Accept': 'text/plain'}
r = requests.post(base_url+f'/league/league1', json=None, headers=headers)
print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))

r = requests.post(base_url+f'/league/league1', json=mockPayload, headers=headers)
print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))