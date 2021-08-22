from flask.json import jsonify
from flask import Flask,render_template, request
from our_utils import *

# This is basically a routing table for all the URIs
# everything resides either in communism_utils or separate modules

## General Srv config

# Initialize flask constructor?
app = Flask(__name__)
db_conn, sql_cursor_obj = connect_db()
logging.basicConfig(filename='test.log', level=logging.INFO)

# Check out more about decorators? 
@app.route('/')
    
def main():
     return render_template('login_template.html')

@app.route('/test')
    
def test_show_text():
    return "You tried to login so hard, but in the end it doesn't matter."

@app.route('/register')

def register_user():
    return render_template('register_template.html')

# Save user to DB, etc, generate user secret
# @app.route('/reg_success')
# def reg_redirect():
#     return "Hello there, mr/mrs [username]! Welcome to our mega-high-tech door opener. Please don't click anything yet."

# def reg_redirect():
#     return "Hello there, mr/mrs [username]! Welcome to our mega-high-tech door opener. Please don't click anything yet."

    
# Route user to authentication and show either wrong creds or home page
@app.route('/login_attempt', methods = ['GET']) #
    
def login_attempt():
    # usr = request.data['username']
    usr_name = request.args['username']
    usr_pass = request.args['pass']
    stub = try_login_user(sql_cursor_obj,usr_name, usr_pass)
    if (stub):
        return render_template('home_page.html')
    else:
        return render_template('error_login.html')
    # print(type(request))
    # username = ""
    # our_utils.get_user_pass_db(sql_cursor_obj,username)
    # return "Trying to log you in but our potatoes are very hot. Just another eon please."

# @app.route('/register_attempt')

# def reg_attempt():
#     return "Some registration is going on."
    
# # Route for logged in users
# @app.route('/home')

# def show_personal_homepage():
#     return "This is your happy place."
