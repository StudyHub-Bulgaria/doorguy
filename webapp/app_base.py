from flask.json import jsonify
from flask import Flask,render_template, request, flash
from utils import *
import jwt

# This is basically a routing table for all the URIs
# everything resides either in utils or separate modules

# Initialize flask constructor 
app = Flask(__name__)

# Setup
db_conn, sql_cursor_obj = connect_db()
app.secret_key = generate_secret_key()

# Enable logging to /tmp/test.log
#logging.basicConfig(filename='/tmp/test.log', level=logging.INFO)

# def token_required(f):
#    @wraps(f)
#    def decorator(*args, **kwargs):
#        token = None
#        if 'x-access-tokens' in request.headers:
#            token = request.headers['x-access-tokens']
 
#        if not token:
#            return jsonify({'message': 'a valid token is missing'})
#        try:
#            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#         #    current_user = Users.query.filter_by(public_id=data['public_id']).first()
#        except:
#            return jsonify({'message': 'token is invalid'})
 
#        return f(current_user, *args, **kwargs)
#    return decorator


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
        # do sessio magic?
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

    return render_template('home_page.html')

app.run(host="0.0.0.0",port=5000)
