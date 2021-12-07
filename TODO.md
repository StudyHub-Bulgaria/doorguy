
# High level todo:

# Software

* Payment integration

    - decide payment processor

    - figure out their API

    - build test environment for their API

* Do security overview
  
    - obvious API bugs

    - OWASP top 10 checklist of each component

    - make _sure_ TLS everywhere

    - make sure user signed code is not easy to brute force

    - check that notification on violations through discord bot work

* Make TLS mandatory on every connection

* Use [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) for signing data inside QR codes.

    - setup/find python ECDSA library

    - generate ECC key pair

    - create API to sign / verify data

    - add hook on user registration to sign user code, save to B

* Add day/night time awareness for camera script - light exposure is very different at 9 a.m. vs 6 p.m. and optimise camera parameters for different ambient light scenarios.

    - have several ambient light conditions
  
    - figure out correct exposure for our size QR codes

* Add redundancy to PIs:

    - if DB is unreachable via LAN, use last known good state from memory.
    - add memory copy of DB.

    - If flash is bad / broken, boot over LAN from server.

* Make sure endpoints are not in the open:

    - firewall rules

    - good credentials

    - only ssh in with keys from local

    - make sure vpn on server is okay

* Add interface for discord bot to actually notify on events (door opened sucess / 3 retries / components offline)

    - async API hook for access granted, access denied (3x), data not signed, etc

* Add healthchecks for all endpoints: 

  - each raspberry (tcp)

  - webapp (tcp,https)

  - authentication backend (tcp,https)

  - door controllers

## Phyiscal

* Design weatherproof box, attatchment to wall

* Setup power cables to PI

* Deploy actual PIs, setup OS, netboot/read flash and overlay RAM fs

* Make sure PI boxes are clean and camera can see through 