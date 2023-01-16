from api import get_leagues_info
from api import get_league
from flask import Flask, render_template, request
from google.cloud import firestore

app = Flask(__name__)

db = firestore.Client()

@app.route('/leagues/<league_name>', methods=['GET'])
def league(league_name):
    league_info = get_league(league_name)
    print(league_info)
    return render_template('league.html', league_info=league_info)

@app.route('/', methods=['GET'])
def home():
    leagues = get_leagues_info()
    print(leagues)
    return render_template('index.html', leagues=leagues)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
