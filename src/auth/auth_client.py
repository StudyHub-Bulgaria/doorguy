### "Thin client" 

import datetime
import logging
import json
import secrets
from ecdsa import SigningKey, VerifyingKey
import requests
import time

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
timeouts = 0

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
    return temp
    # req = json.dumps(temp)

# Send to server
## TODO: Try to send to servere
# on timeout
def send_auth_request(server_ip, port,payload):
    s = 30
    server = "{}:{}".format(server_ip, port)
    req_headers = {}
    r = requests.post(server, 
        headers=req_headers,
        data=json.dumps(payload)
    )

# Ping server every so often
# if it goes down, try backup
# also try to notify me
def heartbeat(server_ip, port):
    timeouts = 0
    max_heartbeats = 5
    backup_ip = "127.0.0.1"
    backup_port = "6040"
    server_uri = "http://{}:{}".format(server_ip, port)
    while (timeouts < max_heartbeats):
        try:
            r = requests.get(server_uri, verify=False, timeout=10)
            print("Server {} is alive.".format(server_uri))
            time.sleep(5)
        except Exception as e:
            print("Server {} timed out: {}".format(server_uri, e))
            timeouts += 1
    
    print("server {} has been down for {} beats, attempting backup".format(server_uri, max_heartbeats))
    return timeouts

    # TODO: If 5 - 10 beats fail, try backup server

## Parse client's QR code - move code from camera_utils here?
def parse_client_code():
    s = 30


## Hearbeat thread - TODO: decide if this should be on a timer in main thread or it's worth a separate thread?
server = "127.0.0.1"
srv_port = "4040"
while(True):
    # print("requesting ",server )
    res = heartbeat(server, srv_port)
    if (res):
        res = heartbeat(backup_ip, backup_port)
        if (res):
            print("Both servers are down. Waiting for servers to come up...")
            break

print("Waiting for servers to be up..")
time.sleep(25)