## StudyHub Doorman 

#### System for entering / exiting StudyHub with just an internet connected phone.

#### High level overview:

Customers register / log in, pay subscription free through _inser_payment_processor_here_ and on home page
get a QR code. Showing the QR code to the reader on the wall will open the door and log the entrance ( exit ).

- Python base app runs on a box inside the library ( debian stable ).
- MySQL backend on same box.
- Has web portal for login / registration.

- On each door is a raspbery pi 4 with a camera,  does some openCV image processing to get unique customer hash
from QR code and maybe sens a open door request to the door.

### Structure

- webapp/ folder contains the web app part that runs on the debian box

- door-iface has the TCP/IP interface stuff for the doors

- rp-client has the stuff that runs on the raspberries to detect and check QRs. 

## To start

For windows, you need to setup python, flask, pip and opencv, which is a pain. 
Also a mysql instance with a specific schema. 

### Docker

Docker images has slim python and dependancies installed.
For now, windows workflow is to use docker:

- install docker;
- docker build;
- docker run;

do arbitrary code changes

- kill old container
- docker build;
- docker run;
- push to github;
