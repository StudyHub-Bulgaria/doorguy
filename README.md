## StudyHub Doorguy

### System for entering / exiting StudyHub with just an internet connected phone.

#### High level overview:

Doorguy is an access control system. It allows customers to buy a subscription through a webpage
and authenticate at your door with a QR code.

For our proof of concept we are using a few Raspberry Pi 4s and the standard raspberry pi cameras v2.

### Architeture

The authenticaiton system uses a server-client architecture. 
The webpage to manage subscriptions is a python Flask app. It can run on a different server than the auth system, as long as both can reach the same DB.

The client (Raspberry) scans and parses QR codes, sends https requests to authentication backend, containing the info parsed from QR code. If the info
matches a user hash (sha512? not decided yet), the client gets an OK response and (the cleint or server? not decided) opens the door.

### Door interface

There are many types of door controllers.
Ours is listening on a tcp socket, accepting specific commands.
When auth is okay, "Open current door" request is sent to door controller.


### Folder Structure

- webapp/ folder contains the web app part that runs on the debian box

- door-iface has the TCP/IP interface stuff for the doors

- rp-client has the stuff that runs on the raspberries to detect and check QRs. 

## Development

Under windows, you will need:
- pythin 3.6+
- pip 
- mysql 

Use pip to install the python dependancies:
pip install -r requirements.txt

### Docker

There's a dockerfile for running the web app - it doesn't contain latest changes!

### Motivation

StudyHub is a 24/7 co-studying (libary-ish) space in Sofia, Bulgaria. 
We have a system with RFID cards that are issued to customers at reception during working hours. With the card,
customers can come in any time they like for the duration of their subscription (weekly, monthly, etc).

We are a volunteer-run organization and the need to have someone in-person there every day for a full 8 hours is getting difficult.
This project is aimed at solving this - it would allow users to buy and manage their subscriptions from a phone (tablet, laptop, etc) 
and authenticate at the door with just a phone.