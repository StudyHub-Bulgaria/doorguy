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

# Get a random 64 byte string in hex
def generate_secret_key():
    return secrets.token_hex()

# hash password with bcrypt and a salt
def hash_user_pass(user_pass):
    salt = bcrypt.gensalt()
    phash = bcrypt.hashpw(user_pass.encode(), salt)
    # return "123"
    return phash
    
def create_user(sql_cursor,usr_name, full_name, phone, email, usr_pass):
    phash = hash_user_pass(usr_pass)

    # create customer in customers
    # create customer account in customer_accounts
    # 

# Read db creds from config and pass them back as a dictionary
def read_db_creds():
    conf = toml.load(".doorguy_config.toml")
    return conf["database"]    

# Remove problematic special characters from string
def escape_user_string(src):
    tmp = src
    re.sub('[^A-Za-z0-9]+', '', tmp)
    return tmp

# Wrapper over SHA512()
# def sha_wrap(src):
#     return hashlib.sha512(src)
    
# Connect to DB and return cursor object to manipulate DB
def connect_db():

    db_creds = read_db_creds()

    cnx = mysql.connector.connect(
        user=db_creds["user"],
        password=db_creds["pass"],
        host=db_creds["host"],
        database=db_creds["db_name"]
    )
    cursor = cnx.cursor()
    return cnx,cursor

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
