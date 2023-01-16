from flask import Flask, request
from google.cloud import firestore
from flask import Flask, request
from flask_restful import Resource, Api
import itertools
from random import shuffle

keys_league_info = ['start_date', 'teams']
keys_team = ['members']

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

leagues_collection = db.collection('leagues')
teams_collection = db.collection('teams')

def get_teams_info():
    out = []
    for team in teams_collection.stream():
        out.append(team.to_dict())
    return out

def get_leagues_info():
    return [doc.id for doc in list(leagues_collection.list_documents())]

def add_results(name_league, teams, result, finals: bool):
    leagues_collection.document(name_league).set({
        'results' if not finals else 'finals': {
            teams: result
        }
    }, { 'merge': True })

def get_team_info(name_team: str):
    return teams_collection.document(name_team).get().to_dict()

def add_team_info(name_team, team_info):
    modified = False
    if get_team_info(name_team) is not None:
        modified = True
    teams_collection.document(name_team).set(team_info)
    return modified

def check_team(team_info: dict):
    members = team_info['members']
    if type(members) is not list or len(members) > 12 or len(members) < 8:
        raise Exception('1')
    for memb in members:
        if type(memb) is not str:
            raise Exception('2')
        if type(memb['ruolo']) is not str or memb['ruolo'] not in ['portiere', 'volante']:
            raise Exception('3')
        if type(memb['name']) is not str:
            raise Exception('5')
    if len([memb for memb in members if memb.get('captain') is not True]) != 1:
        raise Exception('4')
    real_obj = {key: team_info[key] for key in keys_team}
    return real_obj

    
def get_league(name_l: str):
    return leagues_collection.document(name_l).get().to_dict()

def add_league_info(league_info: dict, name_l: str):
    if get_league(name_l) is not None:
        return False
    leagues_collection.document(name_l).set(league_info)
    return True

def check_obj(obj_league):
    if type(obj_league['start_date']) is not str: # check date
        raise Exception('1')
    date = obj_league['start_date']
    comps = date.split('-')
    if len(comps) != 3:
        raise Exception('0')
    if int(comps[0]) < 1900 or int(comps[1]) < 0 or int(comps[1]) > 12 or int(comps[2]) < 0 or int(comps[2]) > 31:
        raise Exception('-1')
    teams: list = obj_league['teams']
    if type(teams) is not list or len(teams) != 8:
        raise Exception('2')
    if len([team for team in teams if len(team) < 2 or len(team) > 64]) > 0:
        raise Exception('3')
    real_obj = {key: obj_league[key] for key in keys_league_info}
    generated_obj = create_groups(teams)
    for key in generated_obj:
        real_obj[key] = generated_obj[key]
    return real_obj

def create_groups(teams: list):
    shuffle(teams)
    out = {}
    out['group_a'] = ["-".join(teams) for teams in list(itertools.combinations(teams[:4], 2))]
    out['group_b'] = ["-".join(teams) for teams in list(itertools.combinations(teams[4:], 2))]
    out['finals'] = ["-".join(["First_Place_A", "Second_Place_B"]), "-".join(["Second_Place_A", "First_Place_B"]), "-".join(["Winner_Semi_1", "Winner_Semi_2"])]
    return out

class CleanResource(Resource):
    def get(self):
        try:
            delete_collection(db.collection('/'), 10)
            return None, 200
        except:
            return None, 400

class LeagueResource(Resource):
    def get(self, league_name):
        try:
            if type(league_name) is not str or len(league_name) < 5 or len(league_name) > 64:
                raise Exception()
            return get_league(league_name), 200
        except:
            return None, 404

    
    def post(self, league_name):
        try:
            if type(league_name) is not str or len(league_name) < 5 or len(league_name) > 64:
                raise Exception()
            data_league = check_obj(request.json)
            if not add_league_info(data_league, league_name):
                return None, 409
            return data_league, 201
        except Exception as e:
            print(e)
            return None, 400

class TeamResource(Resource):
    def post(self, name_team):
        try:
            if type(name_team) is not str or len(name_team) < 5 or len(name_team) > 64:
                raise Exception()
            data_json = check_team(request.json)
            if not add_team_info(name_team, data_json):
                return data_json, 200
            return data_json, 201
        except:
            return None, 400

app = Flask(__name__)
api = Api(app)

basePath = '/api/v1'
api.add_resource(CleanResource, f'{basePath}/clean')
api.add_resource(LeagueResource, f'{basePath}/league/<string:league_name>')
api.add_resource(TeamResource, f'{basePath}/teams/<string:team_name>')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
