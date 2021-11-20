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
    
# Route user to authentication and show either wrong username/password or home page
@app.route('/login_attempt', methods = ['GET']) #
def login_attempt():

    usr_name = request.args['username']
    usr_pass = request.args['pass']

    logged_in = try_login_user(sql_cursor_obj,usr_name, usr_pass)
    if (logged_in):
        # Create random session key for this user
        temp_key = secrets.token_hex()
        sk = base64.b64encode(temp_key.encode())
        session["user"] = sk

        # This is needed for sessions to time out, otherwise the die _only_ on browser closing
        session.permanent = True
        return render_template('home_page.html')
    else:
        flash("Username or Password incorrect.")
        return render_template('login_page.html')

# Route user to registration success and home page or show error message
@app.route('/register_attempt', methods = ['GET', 'POST'])
def register_attempt():
    usr_name = request.form.get('username')
    full_name = request.form.get('name')
    uni = request.form.get('uni')
    phone = request.form.get('phone')
    email = request.form.get('email')
    usr_pass = request.form.get('pass')
    re_pass = request.form.get('re_pass')
    print("pass1: {} pass2: {}".format(usr_pass, re_pass))
    # DO all sorts of valdiations

    res = validate_user_registration_data(usr_name, phone, usr_pass, re_pass)
    if (res == "Success"):
        # return "Sunflowers and sunshine my darling"
        create_user(sql_cursor_obj, usr_name, full_name, phone, email, usr_pass)
    else:
        flash(res)
        return render_template("register_page.html")


# TODO add check that only logged in users access this
# Route for logged in users
@app.route('/home', methods = ['GET'])
def show_personal_homepage():
    ## TODO map this session key to actual user - either through OBJ in memory or write session key to DB
    if "user" in session:
        logged_in_user = session["user"]
        return "{} is logged in.".format(logged_in_user)
    # return render_template('home_page.html')
    else:
        return "You need to login."
app.run(host="0.0.0.0",port=5000)
