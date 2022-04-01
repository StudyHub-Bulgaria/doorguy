from flask.json import jsonify
from flask import Flask,render_template, request, flash, session, redirect, url_for
from datetime import timedelta
from utils import *
import jwt
import os

import logging
import mail_util


## TODO: set coockie expiration

## Configure logger object
web_log = logging.getLogger("vratar_log")

# Create formatter, handlers for stream and for file, set severity
# TODO
# this will make _ALL_ things log there Enable logging to /tmp/test.log
#logging.basicConfig(filename='/tmp/test.log', level=logging.INFO)

# Initialize flask constructor 
app = Flask(__name__)

# Make sessions expire every 15 minutes
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=15)

# database and "session key" stuff
db_conn, sql_cursor_obj = connect_db()
app.secret_key = generate_secret_key()


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
    
# Route user to authentication
# if user logs in successfully, set session key unique to user
# and show either wrong username/password or home page
@app.route('/login_attempt', methods = ['GET']) #
def login_attempt():

    # Fail on requests without password/username
    try:
        usr_name = request.args['username']
        usr_pass = request.args['pass']
    except Exception as e:
        flash("Username or Password incorrect.")
        return render_template('login_page.html')    
    if (not usr_pass):
        flash("Username or Password incorrect.")
        return render_template('login_page.html')
    
    logged_in = try_login_user(sql_cursor_obj,usr_name, usr_pass)
    if (logged_in):
        ## todo save this somewhere
        # Create session for user with some userid as session key / cookie so we can give home page content
        # based on who logged in
        # maybe keep a global dict() of user_sesison_key:user_id? 
        temp_key = secrets.token_hex()
        # temp_key = get_user_uuid(usr_name)
        sk = base64.b64encode(temp_key.encode())
        session["user"] = sk

        # This is needed for sessions to time out, otherwise the die _only_ on browser closing
        session.permanent = True
        # IF flashing here make sure to update home page to ONLY use last flash for img <src>
        return redirect(url_for('show_homepage'))
    else:
        flash("Username or Password incorrect.")
        return render_template('login_page.html')

# Route user to registration success and home page or show error message
@app.route('/register_attempt', methods = ['POST'])
def register_attempt():
    # Parse user data

    print("[DEBUG] Parsing user data ")
    #TODO add class object here
    # TODO fix class creation here
    
    user_data = user_profile()
    try:
        user_data.username = request.form.get('username')
        user_data.real_name = request.form.get('name')
        user_data.university = request.form.get('uni')
        user_data.phone_number = request.form.get('phone')
        user_data.email = request.form.get('email')
        cleartext_pass = request.form.get('pass')
        confirm_pass = request.form.get('re_pass')
    except Exception as e:
        flash("All fields are mandatory")
        return render_template("register_page.html")

    # print("[debug] pass1: {} pass2: {}".format(usr_pass, re_pass))

    # Validate that user entered legitimate data
    res = validate_user_registration_data(user_data, cleartext_pass, confirm_pass)
    if (res == "Success"):
        ret = create_user(sql_cursor_obj, user_data, cleartext_pass)
        
        if (not ret):
            return "Some erros occured during user registration."

        # Actually register user
        return "Sunflowers and sunshine my darling"
    else:
        flash(res)
        return render_template("register_page.html")


# TODO add check that only logged in users access this
# Route for logged in users
@app.route('/home', methods = ['GET'])
def show_homepage():
    ## TODO map this session key to actual user - either through OBJ in memory or write session key to DB
    # as we'd _really_ like to know who logged in, so we can 
    if "user" in session:
        logged_in_user = session["user"]
        # return "{} is logged in.".format(logged_in_user)
        # flash("Welcome bro.")

        # TODO: set variable here to show user qr code
        # Get info on which user from session key?
        user_id = 3
        user_code_location = get_user_code_filename(user_id)
        ## TEST
        # user_code = hashlib.sha512("Some data taht should be encoded".encode()).hexdigest()
        # fqr = generate_user_code("Some data taht should be encoded".encode())
        # flash(fqr)
    
        flash("static/images/{}".format(user_code_location))
        return render_template('home_page.html')
    else:
        return "You need to login."

app.run(host="0.0.0.0",port=5000)
