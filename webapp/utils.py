from datetime import datetime
import mysql.connector
import re
import bcrypt
import hashlib
import logging
import json
import toml
import secrets
import base64
import qrcode

# Get a random 64 byte string in hex
def generate_secret_key():
    return secrets.token_hex()

# hash password with bcrypt and a salt
def hash_user_pass(user_pass):
    salt = bcrypt.gensalt()
    phash = bcrypt.hashpw(user_pass.encode(), salt)
    # return "123"
    return phash

## Wrapper over user creation
# generate user QR code
# save user to DB backend
# return success / error msg 
def create_user(sql_cursor,usr_name, full_name, phone, email, usr_pass):
    phash = hash_user_pass(usr_pass)

    # create customer in customers
    # create customer account in customer_accounts
    return "Sunshine and rainbows"

# Read db creds from config and pass them back as a dictionary
def read_db_creds():
    try:
        conf = toml.load(".doorguy_config.toml")
    except:
        print("[error] Configuration file missing.")
        return

    return conf["database"]    

# Remove problematic special characters from string
def escape_user_string(src):
    tmp = src
    re.sub('[^A-Za-z0-9]+', '', tmp)
    return tmp

# Wrapper over SHA512()
# def sha_wrap(src):
#     return hashlib.sha512(src)
    
# Connect to DB and return cursor object to manipulate DB if success
def connect_db():
    db_creds = read_db_creds()
    try:
        cnx = mysql.connector.connect(
            user=db_creds["user"],
            password=db_creds["pass"],
            host=db_creds["host"],
            database=db_creds["db_name"]
        )
        cursor = cnx.cursor()
        return cnx,cursor
    except:
        print("[error] Could not connect to mysql database. Please check your configuration, if your database is up and if your user has permissions.")
        exit(-2)

# Some sanity checks over user registration input
def validate_user_registration_data(usr_name, phone, usr_pass, re_pass):
    if (usr_name == ""):
        return "Username is required."
    if (usr_pass == "" or re_pass == ""):
        return "Both password fields are required."
    if (usr_pass != re_pass):
        return "Password and confirm password did not match."
    if (len(usr_pass) < 5):
        return "Your password should be at least 5 symbols long. Stronger password rules will be applied soon."

    return "Success"

# TODO: index DB by username
# Get hash of user pass from DB
def get_user_pass_db(sql_cursor, username):
    
    # Because SQL conenctor wants tuples
    user_name = (username,)
    user_id_query = "SELECT customer_id FROM customer_accounts WHERE username = %s"
    sql_cursor.execute(user_id_query, user_name)
    user_id_tuple =  sql_cursor.fetchone()
    if (user_id_tuple == None):
        return None
    
    get_query = ("SELECT password FROM customer_accounts WHERE customer_id = %s")
    sql_cursor.execute(get_query, user_id_tuple)
    user_pass = sql_cursor.fetchone()

    if (user_pass):
        return user_pass[0]
    else:
        return None

def try_login_user(sql_cursor, username, pass_input):

    pass_hash = get_user_pass_db(sql_cursor, username)
    if (pass_hash):
        if (bcrypt.checkpw(pass_input.encode(), pass_hash.encode())):
            return True
        else:
            return False
    return False

def create_log(id, username, door_id):
    time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    stamp = "Date & Time: {}, ID: {}, Username: {}, Door ID: {}".format(time, id, username, door_id)

    #     when utilising this function, make sure to import logging and include the bottom function within the file that you are logging for
    #     logging.basicConfig(filename='<filename>.log', level=logging.INFO)

    logging.info(stamp)


### QR utils

## Final wrapper of user QR code generation. Check docs for more info 
def generate_user_code(input_data):

    # Pass input data into sha wrapper
    uuid_hex = hashlib.sha512(input_data).hexdigest()
    signed_uuid = sign_code(uuid_hex, 0)
    # Sign user code
    user_code = qrcode.make(signed_uuid)
    print("qr code type: {} can do {}".format(type(user_code), dir(user_code)))
    ## caller can save to DB if they wish
    ## TODO: this might have to be a file to show in flask after all
    return user_code


# TODO: Sign a code with the ECDSA signing key
def sign_code(code, signing_key):

    # ECDSA black magic to be implemented
    return code

# Get user QR code from db
def get_user_code(user_id):
    s  = 30
    return "some code value"

# Given user id, get QR code filename from DB
def get_user_code_filename(user_id):
    # Get qr_code_filename from customer SQL()
    return "qrcode_test.png"

# Given username, return user uuid hash from DB
def get_user_uuid(usr_name):
    return "some hash value"