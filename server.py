from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/login')
def on_login():
    # TODO
    # On first login, create new entry to db
    # Otherwise get user details from db


@app.route('/users')
def get_users():
    # TODO
    # Get all all user details


@app.route('/user/<user_id>')
def get_user(user_id):
    # TODO
    # Get specific user info from user_id


@app.route('/bets/<date>')
def get_bets(date):
    # TODO
    # Get all playable bets for a specific date


@app.route('/userbets/<user>/<date>')
def get_userbets(user, date):
    # TODO
    # Get the bet for a specific user on a specific date
