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
from heartbeat import MAX_HB_TIMEOUTS, HEART_RATE, RepeatTimer
from heartbeat import DOORGUY_VER

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
def create_auth_request(data, signature, door_id):
    now = get_timestamp_now()
    temp = {"ver":DOORGUY_VER, "door_id":door_id, "data":data, "sig":signature}
    return temp

# Send auth request to server
def send_auth_request(server_ip, port,payload):
    server_uri = "http://{}:{}/authenticate".format(server_ip, server_port)
    req_headers = {}
    try:
        r = requests.post(server_uri, 
            headers=req_headers,
            json=json.dumps(payload)
        )
    except Exception as e:
        print("[ERROR] Failed to deliver auth request...heartbeats should catch this?")

## Parse client's QR code - move code from camera_utils here?
def parse_client_code():
    s = 30

## Shortcut to sending auth reqeusts - for testing
def request_auth_test():
    global client_id, server_ip, server_port
    data = create_auth_request("some-data", "some-signature-data", client_id)
    f = send_auth_request(server_ip, server_port, data)
    # print("[DBG] sending auth request: ", data)

# Ping server every so often 
# TODO: Add retry and notifications
def send_heartbeat(server_ip, port):
    global srv_timeouts, client_id
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
    print("[autch client {}] running heartbeats and test auth against {}:{}".format(client_id, server_ip, server_port))
    
    ## Start a heartbeat timer
    hb_timer = RepeatTimer(HEART_RATE, send_heartbeat, [server_ip, server_port])
    # hb_timer.start()
    
    # TODO: Do the image processing shit
    # Loop sending auth mesages
    auth_req_timer = RepeatTimer(5, request_auth_test)
    auth_req_timer.start()
main_loop()