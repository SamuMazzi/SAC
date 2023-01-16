import requests
import json

base_url = "https://api-dot-es220224sm.ey.r.appspot.com/api/v1/garden/clean"
# headers = {'Content-type': 'application/json'} #, 'Accept': 'text/plain'}
r = requests.get(base_url)
print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))

#r = requests.post(base_url+f'/car/{uuid2}', json=mockPayload, headers=headers)
#print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))

#r = requests.post(base_url+f'/car/{uuid}', json={}, headers=headers)
#print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))