import time
import random
from matplotlib.font_manager import json_dump
import requests
import json

def example_send_hearbeat_func(ip_addr): 
    timeout = 5
    check_freq = 10

    # Function to send ICMP packet to target.
    # If response doesn't come back in _timeout_ seconds, return error
    example_response_time = example_fake_server_response()
    while (timeout < example_response_time):
        # Sleep for a few seconds beore checking again
        time.sleep(check_freq)
        example_response_time = example_fake_server_response()            
        if (timeout > example_response_time):
            print("Error: Server timed out heartbeat.")
            return -3



# return a random number between 0 and 10
def example_fake_server_response(ip_addr):
    return random.randint % 10


# Send a fake post request to localhost on 4444
def example_send_auth_request(data, srv_ip):
    s = 30
    payload = {"key":"123456123"}
    req_headers = {'content-type': 'application/json'}

    print("Request popup")
    r = requests.post("http://localhost:8000/popup", 
        headers=req_headers,
        data=json.dumps(payload)
    )
    print(r.text)

    print("Request baz")
    r = requests.post("http://localhost:8000/ss", 
        headers=req_headers,
        data=json.dumps(payload)
    )
    print(r.text)

example_send_auth_request("kon", "loaclhost")