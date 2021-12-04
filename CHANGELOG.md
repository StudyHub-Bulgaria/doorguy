## Unreleased 

# Note: this is currently just a TODO list, to be migrated to Github Issue tracker

* Use [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) for signing data inside QR codes.

* Add code generation on user registration, sign code with ECDSA key.

* Add day/night time awareness for camera script - light exposure is very different at 9 a.m. vs 6 p.m. and optimise camera parameters for different ambient light scenarios.

* Add interface for discord bot to actually notify on events (door opened sucess / 3 retries / components offline)

* Add healthchecks for all endpoints: 

- each raspberry (tcp)

- webapp (tcp,https)

- authentication backend (tcp,https)

- door controllers
