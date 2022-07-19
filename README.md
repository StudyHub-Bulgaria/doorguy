## Welcome to StudyHub's doorguy systrem

Doorguy is an access control system. It allows subscribers access a premises just with their mobile phone.

### What is this about

Loosely, the architecture is the following:

We have a [Flask](https://flask.palletsprojects.com/) web for managing subscriptions, and an authentication service.

You can deploy as many clients as you want, where the clients send JSON payloads to be authenticated by the service. If the payload contain valid tokens,
the authentication service sends RPC to a door controller to open the door.

In our case, we deploy clients as a raspberry PI with a camera next to a door.

The user gets the QR code from the webpage, shows it to the camera. After parsing, the camera sends the token from the QR code to auth service.

### Folder Structure

- webapp/ folder contains the web portal for users

- auth/ holds the service for authentication and user management.

- door_interface/ will house the TCP/IP interface stuff for the door controllers

- client/ has the client code to scan QR codes and check against the auth backend.

- docs/ holds developer documentation.

- monitor_announce/ holds utility stuff for noitifcations - email, discord bot

- a config.json file in the webapp folder holds all the server configurations ( DB conenction strings, ports, IPs, etc)

## How to run

Clone this repo:
```
git clone https://github.com/StudyHub-Bulgaria/doorguy.git
```

Pre-requisites for the web-app and auth services: 
> Python 3.6+
> newish mysql or mariadb server 

Use pip (recommended) to install the python dependancies for each component:
```
pip install -r requirements.txt
```

Load the schema file in your DB:
```
mysql -u <user> -h <host> -p <db_name> schema.sql

```
To run each compoennt
```
python run_dev.py 
```

By default you will see the page on http://localhost:5000

[TODO} The webapp, auth service and clients can be deployed on different hosts, networks, geographically. As long as the webapp and auth service can reach the DB, we're good. But for now, 
we'd like to deploy everything on prem as that means we're somewhat resilient to conenction drops - if the internet *dies* users with accounts can still use the service.

## Contributing
Read through the github Issues - they describe on a high level what the roadmap is.
For more specific todos, read through the docs. Each component has a description and todo list with needed APIs and functions.

Github Workflow:

- clone repo
- create feature branch
- open pull request for merging

### Docker
Under construction.

## Hardware
For our proof of concept we are using a few Raspberry Pi 4s and the standard raspberry pi cameras v2 to scan the codes.
The backend authentication and web page services run on a small linux machine and communicates with standard door controllers from a vendor.

### Why

[StudyHub](www.studyhub.bg) is a 24/7 co-studying (libary-ish) space in Sofia, Bulgaria. 
We have a system with RFID cards that are issued to customers at reception during working hours. With the card,
customers can come in any time they like for the duration of their subscription (weekly, monthly, etc).

We are a volunteer-run organization and the need to have someone in-person there every day for a full 8 hours is taking it's toll.
This project is aimed at solving this - it would allow users to buy and manage their subscriptions from a phone (tablet, laptop, etc) 
and authenticate at the door with just a phone.
