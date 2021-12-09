## Welcome to StudyHub's doorguy systrem

Doorguy is an access control system. It allows subscribers to register and open doors by scanning a QR code at the door.

This project has several components:

* Web portal for user

* Authentication backend to check if a given code has been signed 

* Small python script to control raspberry cameras and send requests for authentication

* Discord bot to notify us about any components going offline / repeated access failures.

### Architeture

The authenticaiton system uses a server-client architecture. 
The webpage to manage subscriptions is a python Flask app. It can run on a different server than the auth system, as long as both can reach the same DB.

The clients (Raspberry Pis) parse QR codes, send https requests to authentication backend, containing the info parsed from QR code. If the info
matches a user uuid and is signed with correct ECC key ( to be discussed ) the client gets an OK response and the server requests the controller to open the door.

### Folder Structure

- webapp/ folder contains the web portal for registration and login

- auth/ holds the service for authentication and user management.

- door_interface/ has the TCP/IP interface stuff for the door controllers

- rp_client/ has the script running on the raspberries to scan QR codes and check against the auth backend.

- docs/ holds developer documentation.

- monitor_announce/ holds the discord bot interface and data
 
- .doorguy_config.toml is the main project config ( DB conenction strings, ports, IPs, etc)

- test_data/ contains some test QR codes and a database dump with test
user data.

## How to run

Clone this repo:
```
git clone https://github.com/StudyHub-Bulgaria/doorguy.git
```

Pre-requisites for the web-app: 
> Python 3.6+

> mysql 8 reachable on default port

> DB connection strings are in .doorguy_config.toml

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

Read through the docs. Each component has a description and todo list with needed APIs.

Github Workflow:

- clone repo
- create feature branch
- open pull request for merging

### Docker

TODO: make usable docker image that runs webportal and authentication and another for DB.
Have default configs for docker image, have DB dump with docker DB image.

## Hardware
For our proof of concept we are using a few Raspberry Pi 4s and the standard raspberry pi cameras v2 to scan the codes.
The backend authentication runs on a small linux machine and communicates with standard door controllers from a vendor.


### Motivation

[StudyHub](www.studyhub.bg) is a 24/7 co-studying (libary-ish) space in Sofia, Bulgaria. 
We have a system with RFID cards that are issued to customers at reception during working hours. With the card,
customers can come in any time they like for the duration of their subscription (weekly, monthly, etc).

We are a volunteer-run organization and the need to have someone in-person there every day for a full 8 hours is taking it's toll.
This project is aimed at solving this - it would allow users to buy and manage their subscriptions from a phone (tablet, laptop, etc) 
and authenticate at the door with just a phone.