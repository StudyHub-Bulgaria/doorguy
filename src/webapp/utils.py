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
import time
from ecdsa import SigningKey


## our stuff
from sql_queries import *

# Subscription types
DAILY_SUBSCRIPTION_TYPE = 1
WEEKLY_SUBSCRIPTION_TYPE = 2
MONTHLY_SUBSCRIPTION_TYPE = 3
NONSTUDENT_MONTLY_SUBSCRIPTION_TYPE = 4
SEMESTER_SUBSCRIPTION_TYPE = 5

# TODO create APIs to wrap this and have everything work with user object?
class User_profile():

    def __init__(self, name, username, uuid, pass_hash, email):
        self.real_name = ""
        self.username = ""
        self.uuid = ""
        self.pass_hash = ""
        self.email = ""
        self.university = ""
        self.subscribtion_valid = False
        self.subscribtion_end_date = ""
        self.phone_number = ""
        self.zkteco_id = 0

# TODO Fix up this class
class home_page_data():
    def __init__(self):
        self.real_name = ""
        self.username = ""
        self.subscribtion_valid = False
        self.subscribtion_end_date = ""

# Get a random 64 byte string in hex
def generate_secret_key():
    return secrets.token_hex()

# Hash password with bcrypt and a salt, return a string of the hash
def hash_user_pass(user_pass):
    salt = bcrypt.gensalt()
    phash = bcrypt.hashpw(user_pass.encode(), salt)
    return phash.decode()

# TODO:
## Why am I asking the DB for time??
def get_current_mysql_time(sql_cursor):

    time = time.time()
    return time


# TODO Given the user logged in session cookie, fetch their DB UID
def get_user_uid_from_sessions_key(session_key):

    return 39


## TODO: checkout zkteco id mapping if any
## Wrapper over user creation functoins
def create_user(sql_cursor, user_data, usr_pass, db_conn):
    if (not user_data):
        print("[error] passed EMPTY data to create_user" )
        return None

    print("[debug] Creating user in DB.")
    
    # Create a new user - in the user metadata table
    timestamp = int(time.time())
    user_db_id = create_customer_record_db(sql_cursor, user_data)
    if (not user_db_id):
        print("Inserting a user failed")
        return None

    print("Creating customer account ")
    # Create a new user account tied to this user
    # TODO
    ret = create_customer_account_db(sql_cursor, user_db_id, user_data)

    # TODO: Move user account creationg to a single batch transaction to be rolled/unrolled
    if (not ret):
        print("Creating customer account failed.")
        return None

    print("Try to create customer subscription for user: ", user_db_id)
    create_customer_subscription_db(sql_cursor, user_db_id, timestamp, user_data)
    # TODO: We only commit a transaction if we successfully created a user
    db_conn.commit()
    return user_db_id

    # TODO

CONFIG_FILE = "config.json"

# Read config file
def read_config():
    try:
        with open(CONFIG_FILE) as f:
            raw_data = f.read()
            try:
                creds = json.loads(raw_data)
            except Exception as e:
                print("[error] Invalid config file.")
                exit(-2)
            return creds

    except Exception as e:
        print(e)
        exit(-2)

# Remove problematic special characters from string
def string_clean_non_alphanumeric(src):
    res = ''.join(ch for ch in src if ch.isalnum())
    return res

# Connect to DB and return cursor object to manipulate DB if success
def connect_db():
    conf = read_config()
    if (conf):
        db_creds = conf.get("db_creds")
        print("TRY ", db_creds)
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

# Check if a given user has a subscription already or this is a fresh haccount
def user_has_subscription(sql_cursor,user_id):
    # Check if a user has a valid code to show them
    sql_cursor.execute(USER_HAS_SUBSRIPTION_Q, (user_id,))
    # TODO Execute query

    # if not, show them some generic thing?
    return False


# TODO: implement DB queries
# Change a users password if its valid
def change_user_password(old_pass, new_pass, uid):

    
    return True
    
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
def get_user_pass_db(sql_cursor, user_id):

    sql_cursor.execute(GET_USER_PASSWORD_Q, user_id)
    user_pass = sql_cursor.fetchone()
    if (user_pass):
        return user_pass[0]
    else:
        return None

# Login a user into the system
def try_login_user(sql_cursor, user_name, pass_input):
    sql_cursor.execute(SELECT_CUSTOMER_ID_BY_USERNAME_Q, (user_name,))
    user_id =  sql_cursor.fetchone()
    if (user_id == None):
        return False

    pass_hash = get_user_pass_db(sql_cursor, user_id)
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

## Final wrapper of user QR code generation. Check docs for more info
def generate_user_code(input_data, sign_key):

    uuid_hex = hashlib.sha512(input_data).hexdigest()
    signed_uuid = sign_key.sign(uuid_hex)
    user_code = qrcode.make(signed_uuid)

    # Probably save as file on disk and save file path to DB?
    return user_code

#TODO
# Get user QR code from db given username?
def get_user_qr_code_path_db(username):
    user_code_q = """ SELECT user_qr_code_path FROM customer_accounts JOIN customers WHERE username == %s"""
    # Return the file path for this
    # sql_cursor.execute()
    # path = sql_cursor.fetchone()
    qr_path = "/tmp/user_qr_demo_path"
    return "qr_path"

# TODO: Get user DB index from login token thing
def get_user_id_from_token(sql_cursor, token):
    return token

# Get user subscription expiration timestamp from db
def get_sub_expire_date_db(sql_cursor, user_id):
    sql_cursor.execute(SUBSCRIPTION_EPXIRE_DATE_Q, (user_id,))
    expire_date =  sql_cursor.fetchone()
    return expire_date[0]

# Given user id, get QR code filename from DB
def get_user_code_filename(sql_cursor, user_id):
    sql_cursor.execute(GET_USER_QR_CODE_PATH_Q, (user_id,))
    filename = sql_cursor.fetchone()
    return filename[0]

# Return user UUID from DB by their username
def get_user_id_by_user_name(sql_cursor, usr_name):
    sql_cursor.execute(SELECT_CUSTOMER_ID_BY_USERNAME_Q, (usr_name,))
    user_id = sql_cursor.fetchone()
    return user_id[0]


# Given username, return user uuid hash from DB
def get_user_uuid_db(usr_name):

    return "some hash value"

# Given user name, retrieve customer subscription info
def get_user_subscription_info_db(user_name):

    # TODO
    # user_obj = user()
    # Call APIs to get stuff from DB
    # user_obj.uuid = get_user_uuid()
    # JOIN customers, customer subscriptions, where uuid == uuid
    subscription_info_q = """ SELECT * FROM customer_subscriptions WHERE """

    return None

# TODO: More sophisticated parsing of use rnames - or rename DB to realname thing
# INSERT a user in customers table, return user ID
def create_customer_record_db(sql_cursor, user_data):

    create_customer_q = """INSERT INTO customers (university, first_name, phone, zkteco_id, email) VALUES (%s, %s, %s,%s, %s); """
    data_tuple = (user_data.university, user_data.real_name, user_data.phone_number, user_data.zkteco_id,user_data.email)
    user_id_q = """SELECT LAST_INSERT_ID(); """
    try:
        sql_cursor.execute(create_customer_q, data_tuple)
        print("Customer insrted")
        user_db_id = sql_cursor.execute(user_id_q, ())
        user_db_id = sql_cursor.fetchone()[0]
        print("[DEBUG] User ID: ", user_db_id)
        return user_db_id

    except Exception as e:
        print("[debug] MYSQL error during transaction. User not inserted.")
        print("debug: Exception: {}".format(e))
        return None


# Create an account in customer_accounts
def create_customer_account_db(sql_cursor, user_db_id, user_data):

    add_user_account_q = """INSERT INTO customer_accounts (customer_id, username, password) VALUES (%s, %s, %s);"""
    account_data_tuple = (user_db_id, user_data.username, user_data.pass_hash)
    print("[debug] Customer account: {}".format(account_data_tuple))

    try:
        print("debug: About to execute ", add_user_account_q )
        sql_cursor.execute(add_user_account_q, account_data_tuple)
        print("Account created.")
        return user_db_id
    except Exception as e:
        print("Database error during account creation, account not created: {}".format(e))
        return None



# INSERT default ( empty ) subscription for user
def create_customer_subscription_db(sql_cursor, user_db_id, timestamp, user_data):

    # TODO add subscription active column - or always calcualte on the fly?
    add_user_default_subscription_q = """INSERT INTO customer_subscriptions (customer_id, is_valid, subscription_type, validity_start, validity_end) VALUES (%s, %s, %s, %s, %s);"""
    subscription_tuple = (user_db_id, 0, DAILY_SUBSCRIPTION_TYPE, timestamp, timestamp)
    print("creating subscription with: {}".format(subscription_tuple))
    
    try:
        sql_cursor.execute(add_user_default_subscription_q, subscription_tuple)
        print("Subscription created")
        return True
    except Exception as e:
        print("Database error during account creation, subscription not added: {}".format(e))
        return None
