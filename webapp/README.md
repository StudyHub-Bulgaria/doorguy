## This is the web frontend of the doorguy app.

Users can register, login and update their subscription through this interface.
It is configured with /webapp/.doorguy_config.toml.


### TODO: If using signing process, gen and save signing / verifying keys
## User QR code gen:

1. Hash user data with salt sha512(user_data,salt) to get hexdigest user ID.

2. Sign with ECDSA signing key?

3. Save into DB user code as varchar somewhat big.

4. On visiting homepage, return user code.

5. Have option of easy code regen - hash with new salt, maybe extra random bytes? -> overwrite DB.

6. Should we rotate user codes? 