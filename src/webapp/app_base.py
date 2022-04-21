from flask.json import jsonify
from flask import Flask,render_template, request, flash, session, redirect, url_for
from datetime import timedelta
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
    
    
@app.route("/forgot_password")
def forgot_password():
    return render_template("password_recovery_page.html")


@app.route("/recover_password", methods = ["POST"])
def recover_passwrd():
    user_email = "template@email.none"
    try:
        user_email = request.form.get('email')
    except Exception as e:
        flash("Email is required")
        return render_template("password_recovery_page.html")
    
    flash("A recovery email has been sent to {}. Please check your junk folder if you don't see it.".format(user_email))
    return render_template("password_recovery_page.html")
    
    # TODO: If email is valid
    # Create OTP token, send to email special url
    # Create handler for password resets 
    # only shows good page if OTP token was valid 
    # Save tokens to DB with validity range of 15 mins
    # Afterr success or 15 mins, wipe token?

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
        sk = base64.b64encode(temp_key.encode())
        session["user"] = sk

        # This is needed for sessions to time out, otherwise the die _only_ on browser closing
        session.permanent = True
        # IF flashing here make sure to update home page to ONLY use last flash for img <src>
        return redirect(url_for('show_homepage'))
    else:
        flash("Username or Password incorrect.")
        return render_template('login_page.html')

def parse_register_form(request, user_data):
    user_data.username = request.form.get('username')
    user_data.real_name = request.form.get('name')
    user_data.university = request.form.get('uni')
    user_data.phone_number = request.form.get('phone')
    user_data.email = request.form.get('email')
    cleartext_pass = request.form.get('pass')
    confirm_pass = request.form.get('re_pass')

# Route user to registration success and home page or show error message
@app.route('/register_attempt', methods = ['POST'])
def register_attempt():
    
    global db_conn
    # Parse user data
    print("[DEBUG] Parsing user data ")
    #TODO add class object here
    user_data = user_profile()
    user_data.username = request.form.get('username')
    user_data.real_name = request.form.get('name')
    user_data.university = request.form.get('uni')
    user_data.phone_number = request.form.get('phone')
    user_data.email = request.form.get('email')
    cleartext_pass = request.form.get('pass')
    confirm_pass = request.form.get('re_pass')
    user_data.pass_hash = hash_user_pass(cleartext_pass)
    # TODO: Only hash passwords if they exist and matchm no point otherwise
    #    if (cleartext_pass == confirm_pass):

    # TODO: DO all sorts of valdiations
    res = validate_user_registration_data(user_data, cleartext_pass, confirm_pass)
    if (res == "Success"):
        ret = create_user(sql_cursor_obj, user_data, cleartext_pass, db_conn)
        if (not ret):
            return "Some erros occured during user registration."
        
        # Actually register user
        # flash("Registration success!")
        # return render_template(login_page)
        return "User registration success!"
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
        
        # hacked
        user_code_location = "/static/images/qrcode.png"
        ## TEST
        # user_code = hashlib.sha512("Some data taht should be encoded".encode()).hexdigest()
        # fqr = generate_user_code("Some data taht should be encoded".encode())
        # flash(fqr)
    
        flash(user_code_location)
        return render_template('home_page.html')
    else:
        return "You need to login."
app.run(host="0.0.0.0",port=5000)
