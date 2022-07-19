from flask import Flask,jsonify, request, abort
import datetime
import logging
import json
import secrets
from ecdsa import SigningKey, VerifyingKey
from threading import Thread, Timer

from heartbeat import DOORGUY_VER

# For doors
import sys
sys.path.insert(0,'../')
from door_interface.mock_door_controller import send_req_close, send_req_open

## Configure logger object
# web_log = logging.getLogger("vratar_auth_log")

# Create formatter, handlers for stream and for file, set severity
# TODO
# this will make _ALL_ things log there Enable logging to /tmp/test.log
#logging.basicConfig(filename='/tmp/test.log', level=logging.INFO)

## Only log erros?
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

AUTH_SRV_PORT = 6092

# Initialize flask constructor 
app = Flask(__name__)

# Make sessions expire every 15 minutes
app.config['PERMANENT_SESSION_LIFETIME'] =  datetime.timedelta(minutes=15)

# Setup secret key
app.secret_key = secrets.token_hex()

# Prep ECDSA keys Proof of concept
sk = SigningKey.generate() # Use some nist curve?
vk = sk.verifying_key

def ecdsa_sign_string(sign_key, data):
    sig = sign_key.sign(data.encode())
    return sig

def get_timestamp_now():
    return int(datetime.datetime.timestamp(datetime.datetime.now()))

# Check if validity timestamp in request is okay
def req_timestamp_okay(timestamp):
    now = get_timestamp_now()
    if (now > timestamp):
        return False
    else:
        return True

# Defaul auth endpoint
@app.route('/', methods =['GET','POST'])
def base_auth_endpoitn():
    return {"fake_data":"00005123"}

# Get client id from request20
def process_hearbeat(hb_data):
    now = datetime.datetime.now()
    client_id = hb_data.get("id")
    print("[DBG] ", hb_data)
    print("[{}] Client {} is alive and well".format(now,  client_id))
    
    ## keep stats on the timers
    # If some client fails to respond within like 1-2 mins, notify me

## lect hearbeats from all endpoints
@app.route('/heartbeat', methods =['POST'])
def collect_hearbeats():
    req_data = request.get_json()
    resp = process_hearbeat(req_data)
    return "Okay"

# TODO run a separate logger just for this with custom output
def log_auth_request(auth_data):
    print("[DBG] received auth request: ", auth_data)

def authenticate_request(auth_data):
    sig = auth_data.get("sig")
    print("authentication data: ", sig)
    return True


# Main auth parsing verifying routine
def process_auth_request(auth_data):
    temp = {}
    data = json.loads(auth_data)
    # Log this
    log_auth_request(data)

    # Handle versioning
    ver = data.get("ver")
    if (ver != DOORGUY_VER):
        print("[ERROR] version mismatch server: {} != cleint {}", ver, DOORGUY_VER)
        return abort(500)

    # Check data
    if(authenticate_request(data)):
        # TODO: Call API to open door
        send_req_open(data.get("door_id"))
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'} 

    # TODO: Process auth request?


# Handle auth requests
@app.route('/authenticate', methods =['POST'])
def auth_me():
    resp = {}
    if (request.method == 'GET'):
        resp = {"status": "Invalid request"}
        return json.dumps(resp) 
    else:
        req_data = request.get_json()
        resp = process_auth_request(req_data)
        return resp

app.run(host="0.0.0.0",port=AUTH_SRV_PORT)
