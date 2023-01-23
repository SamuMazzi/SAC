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
real = "https://api-dot-esame20230116sm.ey.r.appspot.com/api/v1"
headers = {'Content-type': 'application/json'} #, 'Accept': 'text/plain'}
r = requests.post(real+f'/consumi/01-11-2023', json={'value': 82}, headers=headers)
print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))

#r = requests.get(real+f'/clean')
#print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))