from __future__ import print_function
import random
import string
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, request, jsonify
app = Flask('Laudrup')

cred = credentials.Certificate('./eurogames-cfbaf-firebase-adminsdk-fq5s1-a186bfdb6a.json')
default_app = firebase_admin.initialize_app(cred, {
    'projectId': 'eurogames-cfbaf'
    })

db = firestore.client()

##### Endpoints #####

@app.route('/create')
def create_user():
    req = request.args.get()
    add_user_to_db(req)

@app.route('/login/<user_id>')
def on_login(user_id):
    user = get_user_from_db(user_id)
    return user
    



@app.route('/users')
def get_users():
    get_users_from_db()
    # Get all all user details


@app.route('/user/<user_id>')
def get_user(user_id):
    get_user_from_db()
    # Get specific user info from user_id


@app.route('/bets/<date>')
def get_bets(date):
    get_bets_from_db(date)
    # Get all playable bets for a specific date


@app.route('/userbets/<user>/<date>')
def get_userbets(user, date):
    get_userbets_from_db(user, date)
    # Get the bet for a specific user on a specific date


@app.route('/bets/add/<date>')
def add_bets(date):
    bets = request.args.get()
    add_bet_to_db(date, bets)
    # Add new bets for a specific date
    # Data for the bets comes from form


@app.route('/leagues/<league_id>')
def get_league(league_id):
    get_league_from_db(league_id)
    # Get league details from league_id


@app.route('/leagues/add')
def add_league(user_id):
    add_league_to_db(user_id)
    # Adds new league
    # Should initially contain owner, "random" join strin and users list


##### Functions connected to Firestore #####

def get_user_from_db(user_id):
    user_ref = db.collection('users').document(user_id)
    user = user_ref.get()
    if user.exists:
        #print("User data: {}".format(user.to_dict()))
        return user.to_dict()
    else:
        #print('No such document')
        return {}
    #user_stream = user_ref.stream()
    # for user in user_stream:
    #    print(f'{user_stream.id} => {user_stream.to_dict()}')


def get_users_from_db():
    users_ref = db.collection('users')
    users_stream = users_ref.stream()

    # for user in users_stream:
    #    print(f'{user.id} => {user.tox_dict()}')

def add_user_to_db(user):
    user_ref = db.collection('users').document(user.user_id)
    user_ref.set({
        u'user_id': user.user_id,
        u'name': user.name,
        u'email': user.email,
        u'leagues': []
    })


def get_bets_from_db(date):
    bets_ref = db.collection('bets').document(date)
    print(bets_ref)
    bets_stream = bets_ref.stream()

    # for bet in bets_stream:
    #    print(f'{bet.id} => {bet.to_dict()}')


def get_userbets_from_db(user_id, date):
    userbets_ref = db.collection('userbets').document(user_id).collection(date)
    userbets_stream = userbets_ref.stream()


def add_bet_to_db(date, bets):
    bet_ref = db.collection('bets').document(date)
    bet_ref.set(bets)


def get_league_from_db(league_id):
    league_ref = db.collection('Leagues').document(league_id)
    league_stream = league_ref.stream()

    # for league in league_stream:
    #    print(f'{league.id} => {league.to_dict()}')


def add_league_to_db(user_id):
    league_id = generate_league_id()
    league_ref = db.collection('Leagues').document(league_id)
    league_ref.set({
        'id': league_id,
        'owner': user_id,
        'members': [user_id]
    })


def add_league_member_to_db(user_id, league_id):
    league_ref = db.collection('Leagues').document(league_id)
    league_stream = db.collection('Leagues').document(league_id)

    # for league in league_stream:
    #    print(f'{league.id} => {league.to_dict()}')


##### Helper functions #####
def generate_league_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])


def main():
    res = add_user_to_db()
    print(res)


if __name__ == '__main__':
    main()


class User:
    def __init__(self, uid, name, email):
        super().__init__()
        self.user_id = uid
        self.name = name
        self.email = email

