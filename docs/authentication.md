## "Backend" authentication system.

Needs to expose APIs for user validation, user saving, changing passwords/ user data.
Thi is separeted from the frontend mostly because:

* if web crashes, user can still authenticate.

* Easier to switch to backup if only this service needs to be configured started.

* Can be run on a different host - allows for both backup and potentially multi-tier backup/replication if is used in more than 1 location. ( Working for more than 1 location is in design todo.)

- API to remove user details after X months of inactivty / GDPR stuff.

- Read GDPR requirements for storing personal data and follow them.

#### Validation API

When client requests validation:

- *if ECDSA is implemented, check signature. Deny not signed data.*