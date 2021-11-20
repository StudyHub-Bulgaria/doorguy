from flask.json import jsonify
from flask import Flask,render_template, request, flash, session
from datetime import timedelta
from utils import *
import jwt
import os

# Initialize flask constructor 
app = Flask(__name__)

# Make sessions expire every 15 minutes
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=15)

# HOld currently logged in users
logged_in_users = []

# database and "session key" stuff
db_conn, sql_cursor_obj = connect_db()
app.secret_key = generate_secret_key()

# Enable logging to /tmp/test.log
#logging.basicConfig(filename='/tmp/test.log', level=logging.INFO)

# Login page 
@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/login')
def login_page():
     return render_template('login_page.html')

# Register page
@app.route('/register')
def register_user():
    return render_template('register_page.html')
    
# Route user to authentication and show either wrong creds or home page
@app.route('/login_attempt', methods = ['GET']) #
def login_attempt():

    usr_name = request.args['username']
    usr_pass = request.args['pass']

    logged_in = try_login_user(sql_cursor_obj,usr_name, usr_pass)
    if (logged_in):
        # Create session key for this user
        temp_key = secrets.token_hex()
        sk = base64.b64encode(temp_key.encode())
        session["user"] = sk
        # logged_in_users.append(sk)
        return render_template('home_page.html')
    else:
        flash("Username or Password incorrect.")
        return render_template('login_page.html')


    # print(type(request))
    # username = ""
    # our_utils.get_user_pass_db(sql_cursor_obj,username)
    # return "Trying to log you in but our potatoes are very hot. Just another eon please."

# Route user to registration success and home page or show error message
# @app.route('/register_attempt')

# TODO add check that only logged in users access this
# Route for logged in users
@app.route('/home')
def show_personal_homepage():
    if "user" in session:
        logged_in_user = session["user"]
        return "{} is logged in.".format(logged_in_user)
    # return render_template('home_page.html')
    else:
        return "You need to login."
app.run(host="0.0.0.0",port=5000)
