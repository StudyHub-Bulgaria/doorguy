from flask.json import jsonify
from flask import Flask,render_template, request
from utils import *

# This is basically a routing table for all the URIs
# everything resides either in utils or separate modules

## General Srv config

# Initialize flask constructor 
app = Flask(__name__)

# Disable db connection for now
#db_conn, sql_cursor_obj = connect_db()

# Enable logging to /tmp/test.log
#logging.basicConfig(filename='/tmp/test.log', level=logging.INFO)

# Login page 
@app.route('/')
def login_page():
     return render_template('login_template.html')

# Register page
@app.route('/register')
def register_user():
    return render_template('register_template.html')
    
# Route user to authentication and show either wrong creds or home page
@app.route('/login_attempt', methods = ['GET']) #
def login_attempt():

    return "This page is temporarily disabled due to DB concerns"

    # usr = request.data['username']
#    usr_name = request.args['username']
#    usr_pass = request.args['pass']

 #   stub = try_login_user(sql_cursor_obj,usr_name, usr_pass)
 #   if (stub):
 #       return render_template('home_page.html')
 #   else:
 #       return render_template('error_login.html')
    # print(type(request))
    # username = ""
    # our_utils.get_user_pass_db(sql_cursor_obj,username)
    # return "Trying to log you in but our potatoes are very hot. Just another eon please."

# Route user to registration success and home page or show error message
# @app.route('/register_attempt')

# Route for logged in users
@app.route('/home')

def show_personal_homepage():

    return render_template('home_page.html')

app.run(host="0.0.0.0",port=5000)
