### "Thin client" 

import datetime
import logging
import json
import secrets
from ecdsa import SigningKey, VerifyingKey

## Configure logger object
# web_log = logging.getLogger("vratar_auth_log")

# Create formatter, handlers for stream and for file, set severity
# TODO
# this will make _ALL_ things log there Enable logging to /tmp/test.log
#logging.basicConfig(filename='/tmp/test.log', level=logging.INFO)

### Global config stuff - to get from config
server_ip = "127.0.0.1"
server_port = "6902"
backup_ip = "127.0.0.1"
backup_port = "6040"

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

# Created request is valid for 15 mins
## Schema loosely like timestamp, door id, 
def create_auth_request(user_name, data, signature, door_id):
    now = get_timestamp_now()
    temp = {"timestamp": now, "door_id":door_id, "sig":signature}
    req = json.dumps(temp)
    return req

# Send to server
## TODO: Try to send to servere
# on timeout
def send_auth_request(server_ip):
    s = 30

# Ping server every so often
# if it goes down, try backup
# also try to notify me
def heartbeat(server_ip):
    s = 0

## Parse client's QR code - move code from camera_utils here?
def parse_client_code():
    s = 30