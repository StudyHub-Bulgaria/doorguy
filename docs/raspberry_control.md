## Each raspberry runs a thin linux with a python script to control the camera. 

## Light modes

Because ambient light differs greatly morning to evenning and are taking pictures of the QR codes, we need to account for ambient light. In very bright ambient light, reduce exposure, in dark evenings increase exposure to get clearer picture.

## To Do:

#### Initialization

On start, read configuration, parse config.toml file and take server IPs.
Ping server - send icmp echo or similar. If not, got to backup server.
Get correct time, setup light mode, start scanning.
If both servers are down, send email to maintainers and try again in 30 seconds. Only send the email first time.

#### Healthcheck API

If the backend server goes down, we need to know to switch to backup.

Ping the server at regular intervals (10 seconds or similar) - probably inside python itself. 
If the server starts timinig out responses, drop connection, negotiate TLS with backup server
and start authenticating against that. Get both main and backup server IP from config.

#### Control loop:

- Script should try to detect QR codes from camera images with qrcode library at some reasonable intervals ( 1 per second or something similar ).
- If a valid QR code is detected, using python's qrcode library parse user data. Send data with validation API

#### Light modes:

Check average ambient light for morning, noon, evening, night for winter/summer. Need to take a camera to location to do tests.
- implement 3/4/5 light modes: very dark, mild/cloudy and bright that rotate at set hours (7:00, 13:00, 17:00 etc). Play with exposure times in a dark/bright room to get sharpest image. Test with generated data from test_data/.

#### Valdiation API:

API to send user data over https to backend auth system.

- Make/Find API for sending http requests back and forth.
- Setup TLS for http conenction with backend auth system.
- Make parser for responses from server (acces granted/ denied, reason, etc).

