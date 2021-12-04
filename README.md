## Welcome to StudyHub's doorguy systrem

Doorguy is an access control system. It allows subscribers to register and open doors by scanning a QR code at the door.

This project has several components:

* Web portal for user

* Authentication backend to check if a given code has been signed 

* Small python script to control raspberry cameras and send requests for authentication

### Architeture

The authenticaiton system uses a server-client architecture. 
The webpage to manage subscriptions is a python Flask app. It can run on a different server than the auth system, as long as both can reach the same DB.

The client (Raspberry) scans and parses QR codes, sends https requests to authentication backend, containing the info parsed from QR code. If the info
matches a user hash (sha512? not decided yet), the client gets an OK response and (the cleint or server? not decided) opens the door.

### Folder Structure

- webapp/ folder contains the web portal for registration and login

- door_interface has the TCP/IP interface stuff for the door controllers

- rp_client has the script running on the raspberries to scan QR codes and check against the auth backend.

- docs holds developer documentation. [TODO]

- .doorguy_config.toml is the main project config ( DB conenction strings, ports, IPs, etc)

## How to run

Clone this repo:
```
git clone https://github.com/StudyHub-Bulgaria/doorguy.git
```

Pre-requisites for the web-app: 

> Python 3.6+
> mysql 8

Use pip to install the python dependancies:
```
pip install -r requirements.txt
```

Run from /webapp
```
python app_base.py 
```

By default you will see the page on http://localhost:5000

## Contributing


Github Workflow:
- a
- b
- +c

### Docker

TODO: make usable docker image

## Hardware
For our proof of concept we are using a few Raspberry Pi 4s and the standard raspberry pi cameras v2 to scan the codes.
The backend authentication runs on a small linux machine and communicates with standard door controllers from a vendor.


### Motivation

StudyHub[www.studyhub.bg] is a 24/7 co-studying (libary-ish) space in Sofia, Bulgaria. 
We have a system with RFID cards that are issued to customers at reception during working hours. With the card,
customers can come in any time they like for the duration of their subscription (weekly, monthly, etc).

We are a volunteer-run organization and the need to have someone in-person there every day for a full 8 hours is taking it's toll.
This project is aimed at solving this - it would allow users to buy and manage their subscriptions from a phone (tablet, laptop, etc) 
and authenticate at the door with just a phone.