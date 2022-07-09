## This is a simple authentication service.


### Auth service
Process authenticaiton requests from clients.
They come as HTTP JSON payloads.

Schema loosely like: A timestamp, door ID, ecc-dsa signed user data.
If signature is okay, return OK response. Send a request to door interface for opening. Log access attempt  
Else, deny response. Log access attempt.

### Auth client
- Runs on the PIs
- Parses QR codes
- creates and sends auth requests?
- does not interact with door at all, because it's outside and can be tampered with
- Graceful fail-over to backup server
- Notify when server is down

### TODO:
- What about that plan to have the DB in memory in case the server dies? - maybe rely that the machines dont die - if they die, outage until we get there
- Make sure tampering with cleint can't fuck up server
- Schema for responses
- API interface for door handling code
- Door handling code
- Where to keep the door code?