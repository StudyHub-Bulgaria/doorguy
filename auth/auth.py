
## This will be our "Backend Authentication system".
# More like a glorified API for valdiating ECDSA signed data
import ecdsa

# Validate a ecdsa signed base64 string?
def validate_string(src, verifying_key):
    # Do ecdsa magic
    s = 30
    return "invalid, mid construction"

# Same but for binary data?
def validate_data(src, verifying_key):
    s = 40
    return 0

