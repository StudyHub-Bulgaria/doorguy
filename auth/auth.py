
## This will be our "Backend Authentication system".
# More like a glorified API for valdiating ECDSA signed data
from ecdsa import SigningKey


# Mostly todos

# Validate a ecdsa signed base64 string?
def validate_string(src, verifying_key):
    # Do ecdsa magic
    s = 30
    return "invalid, mid construction"

# Same but for binary data?
def validate_data(src, verifying_key):
    s = 40
    return 0

# Generate a temporary key pair to sign some stuff for testing
def generate_sign_key_pair_test(): 
    sk = SigningKey.generate() # Use some nist curve?
    vk = sk.verifying_key

    signature = sk.sign(b"test message")

#    print("Message signed")
#    print(signature)
#    assert vk.verify(signature, b"test message")

    return sk

def verification_demo():
    k = generate_sign_key_pair_test()
    vk = k.verifying_key
    m = "This is a test message. "
    m2 = "This is a different message"
    sg = k.sign(m2.encode())
    print(type(sg))
    print(m)
    
    try:
        vk.verify(sg,m.encode())
        print("Verification okay, calling api")
    except:
        print("Verification Failed")


verification_demo()
