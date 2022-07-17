### "Thin client" 

import datetime
import logging
import json
from random import randint
import secrets
from ecdsa import SigningKey, VerifyingKey
import requests
import time

from os import getenv

# Timer stuff
from heartbeat import MAX_HB_TIMEOUTS, HeartBeat, HEART_RATE

### Global config stuff - to get from config
server_ip = "127.0.0.1"
server_port = "6092"
client_id = 0
srv_timeouts = 0

# Get client id from environment
def get_client_id():
    me = getenv("CLIENT_ID")
    if not me:
        print("Client ID not set, randomizing")
        return randint(50,100)
    return int(me)

def ecdsa_sign_string(sign_key, data):
    sig = sign_key.sign(data.encode())
    return sig

def get_timestamp_now():
    return int(datetime.datetime.timestamp(datetime.datetime.now()))

## Schema loosely like timestamp, door id, 
def create_auth_request(user_name, data, signature, door_id):
    now = get_timestamp_now()
    temp = {"timestamp": now, "door_id":door_id, "sig":signature}
    return temp
    # req = json.dumps(temp)

# Send auth request to server
def send_auth_request(server_ip, port,payload):
    s = 30
    server = "{}:{}".format(server_ip, port)
    req_headers = {}
    r = requests.post(server, 
        headers=req_headers,
        data=json.dumps(payload)
    )

## Parse client's QR code - move code from camera_utils here?
def parse_client_code():
    s = 30

# Created request is valid for 15 mins
def create_auth_request(user_name,data, signature):
    now = get_timestamp_now() + 900
    temp = {"validity": now, "username":user_name,"data":data, "sig": signature}
    return json.dumps(temp)


# Ping server every so often 
# TODO: Add retry and notifications
def send_heartbeat(server_ip, port):
    global srv_timeouts, client_id
    print("[DBG] trying to hit server ", server_ip)
    server_uri = "http://{}:{}/heartbeat".format(server_ip, server_port)
    try:
        r = requests.post(server_uri, verify=False, timeout=2, json={"id":client_id})
    except Exception as e:
        # print("Server {} timed out: {}, doing re-try stuff".format(server_uri, e))
        srv_timeouts += 1
        if (srv_timeouts >= MAX_HB_TIMEOUTS):
            print("[ERROR] Seems like the main server is down for {} beats. Will attempt backup, or shutting down..".format(srv_timeouts))
            exit(1)   

    return 1


## main loop of scanning for clients
def main_loop():
    global server_ip, server_port, client_id
    client_id = get_client_id()
    print("[autch client {}] running just heartbeats against {}:{}".format(client_id, server_ip, server_port))
    
    ## Start a heartbeat timer
    timer = HeartBeat(HEART_RATE, send_heartbeat, [server_ip, server_port])
    timer.start()
    
    # Do the image processing shit

main_loop()