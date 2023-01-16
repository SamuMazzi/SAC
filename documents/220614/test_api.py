import requests

mockPayload = {
    "teams": ["aaa", "bfbsd", "casc", "dcsdc", "erfvds", "fascsa", "gdfdas", "hte"],
    "start_date": "2022-11-22"
}
base_url = "http://127.0.0.1:8080/api/v1"
headers = {'Content-type': 'application/json'} #, 'Accept': 'text/plain'}
r = requests.post(base_url+f'/league/league1', json=None, headers=headers)
print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))

r = requests.post(base_url+f'/league/league1', json=mockPayload, headers=headers)
print('I get: ' + str(r.json()) + ' Code: ' + str(r.status_code))