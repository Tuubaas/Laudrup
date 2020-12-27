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
    res = get_users_from_db()
    return res
    # Get all all user details


@app.route('/user/<user_id>')
def get_user(user_id):
    res = get_user_from_db(user_id)
    return res
    # Get specific user info from user_id


@app.route('/bets/<date>')
def get_bets(date):
    res = get_bets_from_db(date)
    return res
    # Get all playable bets for a specific date


@app.route('/userbets/<user>/<date>')
def get_userbets(user, date):
    res = get_userbets_from_db(user, date)
    return res
    # Get the bet for a specific user on a specific date


@app.route('/bets/add/<date>')
def add_bets(date):
    bets = request.args.get()
    add_bet_to_db(date, bets)
    # Add new bets for a specific date
    # Data for the bets comes from form


@app.route('/userbets/add/<user>/<date>')
def add_userbets(user, date):
    userbets = request.args.get()
    add_userbets_to_db(user, date, userbets)


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
        print(user)
        return user.to_dict()
    else:
        return {}


def get_users_from_db():
    users_ref = db.collection('users')
    users_stream = users_ref.stream()
    user_objects = [user.to_dict() for user in users_stream]
    return user_objects

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
    bets = bets_ref.get()
    if bets.exists:
        return bets.to_dict()
    else:
        return {}


def get_userbets_from_db(user_id, date):
    userbets_ref = db.collection('users').document(user_id).collection('bets').document(date)
    userbets = userbets_ref.get()
    if userbets.exists:
        return userbets.to_dict()
    else:
        return {}


def add_bet_to_db(date, bets):
    bet_ref = db.collection('bets').document(date)
    bet_ref.set(bets)

def add_userbets_to_db(user_id, date, bets):
    userbets_ref = db.collection('users').document(user_id).collection('bets').document(date)
    userbets_ref.set(bets)


def get_league_from_db(league_id):
    league_ref = db.collection('leagues').document(league_id)
    league = league_ref.get()
    if league.exists:
        return league.to_dict()
    else:
        return {}


def add_league_to_db(user_id, league_name):
    league_id = generate_league_id()
    league_ref = db.collection('leagues').document(league_id)
    league_ref.set({
        u'id': league_id,
        u'owner': user_id,
        u'name': league_name,
        u'members': [user_id]
    })
    user_ref = db.collection('users').document(user_id)
    user_ref.update({u'leagues': firestore.ArrayUnion([league_id])})


def add_league_member_to_db(user_id, league_id):
    league_ref = db.collection('leagues').document(league_id)
    league_ref.update({u'members': firestore.ArrayUnion([user_id])})


##### Helper functions #####
def generate_league_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])


def main():
    res = get_league_from_db('uhJ85rcI')
    print(res)


if __name__ == '__main__':
    main()

