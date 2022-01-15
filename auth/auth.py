
## This will be our "Backend Authentication system".
# More like a glorified API for valdiating ECDSA signed data
from ecdsa import SigningKey

# Mostly todos
# Generate a temporary key pair to sign some stuff for testing
def generate_sign_key_pair_test(): 
    sk = SigningKey.generate() # Use some nist curve?
    vk = sk.verifying_key

    signature = sk.sign(b"test message")

#    print("Message signed")
#    print(signature)
#    assert vk.verify(signature, b"test message")

    return sk

# Verify a chunk of binary data signed wit ha key
## Data should be encoded to UTF-8 or sth?
def verify_signed_string_data(vk, data, signature):
    try:
        vk.verify(signature,data.encode())
        print("Verification okay, calling api")
    except:
        print("Verification Failed")

# Verify a chunk of binary data signed wit ha key
## How do you encode binary data for ecdsa API?
def verify_signed_binary_data(vk, data, signature):
    try:
        vk.verify(signature,data.encode())
        print("Verification okay, calling api")
    except:
        print("Verification Failed")

# Sign a string with ECC key, return signature
def ecdsa_sign_string(sign_key, data):
    sig = sign_key.sign(data.encode())
    return sig

def ecdsa_sign_binary_data(sign_key, data):
    sig = sign_key.sign(data)
    return sig

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

