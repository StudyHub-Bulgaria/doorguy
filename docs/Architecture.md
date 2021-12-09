## This describes our overall architecture.

Components:

* Web interface for users, where they can register and manage subscription. Home page shows them some stats, end date of subscription, QR code used to authenticate when entering.

* Clients - raspberry PI or similar board, running embedded linux with attatched camera. 
Scans QR codes and communicates with backend for authentication. Each door has a client
on both sides, for entering and leaving.

* Backend authentication - exposes APIs for clients to authenticate users.

* MySQL Database - keeps user records, logs, etc.  

* Discord bot / notification - script to notify maintainers of important events like:

    - some component died.

    - somebody failed to login 300 times in 1 minute.

    - other suspicious authentication activity.

    - reports some stats in intervals.