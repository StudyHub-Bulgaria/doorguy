## Web portal for users to manage account / subscription.

Takes configuration from .doorguy_config.toml
static/ holds all the images, css and other web assets.

From landing page, users can login, resgiter or read user guide.
From home page, user can see end of subscription, QR code for authentication, 
renew subscription button, change password button.

## To Do:

- Make sure home page is only accessible if user is logged in.

- Add more validation to user registration.

- On user registration, hash and save user password and account details in database. 
Create user UUID and save in DATABASE. Save timestamp.

- Create API to rotate user codes:
On login, get user UUID, some random characters. Hash / Base64 encode, figure out good format.
If ECDSA is implemented, sign user code. ( how to show generated data as image tag? - dont want to write / delete files all the time). If user logs in and authenticates, prepare to generate new QR code on next login / refresh. *This section needs some more design work.*

- Add API to flag user codes as *used* if they will be one-time only and regenrated.

- Create user guide. Ask people if user guide is sane and easy to follow.

- Add change password button. Implement change password function.

- Make home page pretty.

- Add renew subscription button. Negotiate details with payment processor. DO NOT leave API keys around in repo. Create API to renew subscription dates and validity flag to use with payment processor API. 


## Decide on these 

1. Hash user data with salt sha512(user_data,salt) to get hexdigest user ID.

2. Sign with ECDSA signing key?

3. Save into DB user code as varchar somewhat big.

4. On visiting homepage, return user code.

5. Have option of easy code regen - hash with new salt, maybe extra random bytes? -> overwrite DB.

6. Should we rotate user codes? 