import requests
import json

with open('mockPayload.json') as json_file:
    mockPayload = json.load(json_file)
uuid = "0a7b27c9-6413-4768-94c4-732309c67caa"
uuid2 = "fce45e62-b76c-490a-897c-9a7daadbf978"
base_url = "http://127.0.0.1:8080/api/v1"
headers = {'Content-type': 'application/json'} #, 'Accept': 'text/plain'}
r = requests.post(base_url+f'/car/{uuid}', json=None, headers=headers)
print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))

r = requests.post(base_url+f'/car/{uuid2}', json=mockPayload, headers=headers)
print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))

r = requests.post(base_url+f'/car/{uuid}', json={}, headers=headers)
print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))