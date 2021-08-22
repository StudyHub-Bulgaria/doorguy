## StudyHub Doorman 

#### System for entering / exiting StudyHub with just a phone.

##### Based on python, raspberries and a door controller that talks TCP/IP.

Note: The raspberry hardware is quite overkill for this.

- Python base app runs on a box inside the library.
- Users can log in through web portal (porta.studyhub.bg or similar), register, pay subscription and get QR code.

- On each door is a raspbery pi 4 with a camera, detects QR code and matches QR strign against hash in DB. 
- If match is found, tell door controller to open door.


### Structure

- webapp/ folder contains the web app part
- door_iface has the TCP/IP interface stuff for the doors
- rp_client has the stuff that runs on the raspberries to detect and check QRs. 
