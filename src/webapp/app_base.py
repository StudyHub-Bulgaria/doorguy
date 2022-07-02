from flask.json import jsonify
from flask import Flask,render_template, request, flash, session, redirect, url_for
from datetime import timedelta
import datetime

from utils import *
import jwt
import os

import logging
import mail_util


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
#  and show either wrong username/password or home page
@app.route('/login_attempt', methods = ['GET']) #
def login_attempt():

    usr_name = request.args['username']
    usr_pass = request.args['pass']

    logged_in = try_login_user(sql_cursor_obj,usr_name, usr_pass)
    if (logged_in):
        ## todo save this somewhere
        # Create session for user with some userid as session key / cookie so we can give home page content
        # based on who logged in
        # maybe keep a global dict() of user_sesison_key:user_id? 
        temp_key = secrets.token_hex()
        # temp_key = get_user_uuid(usr_name)

        ## TODO:
        # sk = base64.b64encode(temp_key.encode())
        ## TODO: set UUIDs in to foreign DB
        session["user"] = get_user_id_by_user_name(sql_cursor_obj, usr_name)

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

    user_data = User_profile("","","","","")
    user_data.username = request.form.get('username')
    user_data.real_name = request.form.get('name')
    user_data.university = request.form.get('uni')
    user_data.phone_number = request.form.get('phone')
    user_data.email = request.form.get('email')
    cleartext_pass = request.form.get('pass')
    confirm_pass = request.form.get('re_pass')

    # print("[debug] pass1: {} pass2: {}".format(usr_pass, re_pass))

    # DO all sorts of valdiations
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
        user_id = logged_in_user
        qr_fnmae = get_user_code_filename(sql_cursor_obj, user_id)
        qr_loc = "/static/images/{}".format(qr_fnmae)
        print("Used qr code location: ", qr_loc)

        # Setup some data to be shown in pag
        user_data = "Some user data to be accesed"
        full_name = "John Doe 361"

        data = {}
        data["username"] = "johndoe361"

        user_id = logged_in_user
        if (not user_id):
            print("HUGE ERROR, USER ID NOT FOUND")
            
        timestamp = get_sub_expire_date_db(sql_cursor_obj, user_id)
        human_date = datetime.fromtimestamp(timestamp).isoformat()
        data["date_expire"] = human_date
        data["qr_loc"] = qr_loc

        # data["email"] = "johndoe@abv.bg"
        ## TEST
        # user_code = hashlib.sha512("Some data taht should be encoded".encode()).hexdigest()
        # fqr = generate_user_code("Some data taht should be encoded".encode())
    
        # flash(user_code_location)
        return render_template('home_page.html', full_name=full_name, data=data)
    else:
        flash("You need to login.")
        return render_template('login_page.html')

@app.route('/forgot_password', methods = ['GET', 'POST'])
def show_forgot_pass_page():
	if request.method == "GET":
		return render_template("password_recovery_page.html")
	if  request.method == "POST":
		email = "dummy@no.domain"
		flash("A recovery email has been sent to {}".format(email))
		return render_template("password_recovery_page.html")

def show_login_access_denied():
    flash("You need to be logged in.")
    return render_template("login_page.html")

@app.route('/manage_subscription')
def show_manage_sub_page():
    if "user" in session:
        return render_template("subscription_management_page.html")
    else:
        return show_login_access_denied()

@app.route('/change_password', methods = ['GET', 'POST'])
def show_change_pass_page():

    # TODO: This has to be behind auth
    if (request.method == "GET"):
        if "user" in session:
            logged_in_user = session["user"]
            return render_template("change_pass_page.html")
        else:
           return show_login_access_denied()
    if (request.method == "POST"):
        if "user" in session:
            flash("This feature is currently under construction.")
            
            # TOOD: Get user pass from db, validate old pass, update to new pass if okay
            logged_in_user = session["user"]

            
            return render_template("change_pass_page.html")
        else:
            flash("You need to be logged in.")
            return render_template("login_page.html")

@app.route('/how-it-works', methods= ['GET'])
def show_guide_page():
    return render_template("how_to_page.html")


app.run(host="0.0.0.0",port=5000)
