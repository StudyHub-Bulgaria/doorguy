from flask import Flask,jsonify,render_template, request, flash, session, redirect, url_for
import datetime
import logging
import json
import secrets

## Configure logger object
# web_log = logging.getLogger("vratar_auth_log")

# Create formatter, handlers for stream and for file, set severity
# TODO
# this will make _ALL_ things log there Enable logging to /tmp/test.log
#logging.basicConfig(filename='/tmp/test.log', level=logging.INFO)

# Initialize flask constructor 
app = Flask(__name__)

# Make sessions expire every 15 minutes
app.config['PERMANENT_SESSION_LIFETIME'] =  datetime.timedelta(minutes=15)

# Setup secret key
app.secret_key = secrets.token_hex()


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
@app.route('/', methods =['POST'])
def base_auth_endpoitn():

    resp = {}
    if (request.method == 'GET'):
        resp = {"status": "Invalid request"}
        return json.dumps(resp) 
    else:
        req_data = request.get_json()
        return "You sent data"


# Main auth routine
def authenticate_request(auth_data):
    temp = {}
    timestamp = auth_data.get("validity")
    if (not timestamp):
        temp["status"] = "fail"
        temp["reason"] = "Timestamp invalid"
        return temp
    else:
        reason = req_timestamp_okay(int(timestamp))
        if (reason):
            temp["status"] = "ok"
            temp["reason"] = "Validity ok"
        else:
            temp["status"] = "fail"
            temp["reason"] = "Validity timestamp expired"
        return temp

@app.route('/authenticate', methods =['POST'])
def auth_me():

    resp = {}
    if (request.method == 'GET'):
        resp = {"status": "Invalid request"}
        return json.dumps(resp) 
    else:
        req_data = request.get_json()
        resp = authenticate_request(req_data)

        return jsonify(resp)


app.run(host="0.0.0.0",port=4000)
