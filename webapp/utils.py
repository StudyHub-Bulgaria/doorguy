from datetime import datetime, time
from os import times
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

# Subscription types
DAILY_SUBSCRIPTION_TYPE = 1
WEEKLY_SUBSCRIPTION_TYPE = 2
MONTHLY_SUBSCRIPTION_TYPE = 3
NONSTUDENT_MONTLY_SUBSCRIPTION_TYPE = 4
SEMESTER_SUBSCRIPTION_TYPE = 5

# Todo create APIs to wrap this and have everything work with user object?
class user_profile():
    def __init__(self):
        self.real_name = ""
        self.username = ""
        self.uuid = ""
        self.pass_hash = ""
        self.email = ""
        self.university = ""
        self.subscribtion_valid = False
        self.subscribtion_end_date = ""
        self.phone_number = ""
    # real_name = ""
    # username = ""
    # uuid = ""
    # pass_hash = ""
    # subscribtion_valid = False
    # subscribtion_end_date = ""
    # email = ""

# Get a random 64 byte string in hex
def generate_secret_key():
    return secrets.token_hex()

# hash password with bcrypt and a salt
def create_user_pass_hash(user_pass):
    salt = bcrypt.gensalt()
    phash = bcrypt.hashpw(user_pass.encode(), salt)
    return phash


def get_current_mysql_time(sql_cursor):

    time_q = "SELECT CURRENT_TIMESTAMP()"
    sql_cursor.execute(time_q)
    timestamp = sql_cursor.fetchone()
    return timestamp

## TODO: checkout zkteco id mapping if any
## Wrapper over user creation functoins
def create_user(sql_cursor, user_data, usr_pass):

    if (not user_data):
        print("[error] passed EMPTY data to create_user" )
    print("[debug] Creating user in DB.")
    phash = create_user_pass_hash(usr_pass)

    # Get current mysql time
    timestamp = get_current_mysql_time(sql_cursor)

    # create customer in customers, get the ID of record we just inserted
    create_customer_q = """INSERT INTO customers (university, real_name, phone, email) VALUES (%s, %s, %s, %s); SELECT LAST_INSERT_ID();"""
    data_tuple = (user_data.university, user_data.real_name, user_data.phone_number, user_data.email)
 
    print("[debug]: About to execute ", create_customer_q)
    try:
        sql_cursor.execute(create_customer_q, data_tuple)
        sql_cursor.fetchall()
        print("executed?")
        user_db_id = sql_cursor.lastrowid
        print("Last row: ", user_db_id)

    except Exception as e:
        print("[debug] MYSQL error during transaction. User not inserted.")
        print("debug: Exception: {}".format(e))
        return None
    print("[debug] creating user okay ")
    
    # if it went through okay, add other customer records
    add_user_account_q = """INSERT INTO customer_accounts (customer_id, username, password VALUES (%s, %s, %s);"""
    account_data_tuple = (user_db_id, user_data.username, user_data.pass_hash)
    print("debug: About to execute ", add_user_account_q )

    try:
        sql_cursor.execute(add_user_account_q, account_data_tuple)
        sql_cursor.fetchone()
    except Exception as e:
        print("[debug] MYSQL errored during transaction. User Account not created.")
        print(e)
        return None

    print(["[debug] user account okay"])

    # Create customer subscription

    # TODO add subscription active column
    add_user_default_subscription_q = """INSERT INTO customer_subscriptions (CUSTOMER_ID, is_valid, subscription_type, validity_start, validity_end) VALUES (%s, %s, %s, %s, %s);"""
    subscription_tuple = (user_db_id, 0, DAILY_SUBSCRIPTION_TYPE, timestamp, timestamp) 
    
    try:
        sql_cursor.execute(add_user_default_subscription_q, subscription_tuple)
    except:
        print("[debug] MYSQL errored during transaction. User Subscription not created.")
        return None

    print("User subscription created. Returning gracefully.")
    # save password etc
    return "Sunshine and rainbows. User added succesfully."

# Read db creds from config and pass them back as a dictionary
def read_db_creds():
    try:
        conf = toml.load(".doorguy_config.toml")
    except:
        print("[error] Configuration file missing.")
        return

    return conf["database"]    

# Remove problematic special characters from string
def string_clean_non_alphanumeric(src):
    res = ''.join(ch for ch in src if ch.isalnum())
    return res

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
        cursor = cnx.cursor(buffered=True)
        return cnx,cursor
    except:
        print("[error] Could not connect to mysql database. Please check your configuration, if your database is up and if your user has permissions.")
        exit(-2)

# Some sanity checks for user password
def validate_user_password(usr_pass, re_pass):
    print("[debug] Validating user password: ", usr_pass)

    if (usr_pass != re_pass):
        return "Both password fields are required."

    if (len(usr_pass) < 5):
        return "Your password should be at least 5 symbols long. Stronger password rules will be applied soon."

    bad_symbols = re.match(r'[\'\"\\]', usr_pass)
    return bad_symbols


# Some sanity checks over user registration input
def validate_user_registration_data(user_data, input_pass, confirm_pass):
    
    if (not user_data.username):
        print("Username given: ", user_data.username)
        return "Username is required."

    if (not user_data.phone_number or len(user_data.phone_number) < 7):
        return "Phone number too short."

    if (not user_data.email):
        return "Invalid email."

    # Validate passwords
    res = validate_user_password(input_pass, confirm_pass)
    if (res):
        return res

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

# Given user id or name something, give us all subscriptioninfo on custoemr 
def get_user_subscription_info(user_name):

    user_obj = user()
    # Call APIs to get stuff from DB
    user_obj.uuid = get_user_uuid()
    # ETC

    return user_obj

