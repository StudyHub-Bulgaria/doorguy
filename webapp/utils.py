from datetime import datetime
import mysql.connector
import re
import hashlib
import logging
import json
import toml

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
def sha_wrap(src):
    return hashlib.sha512(src)
    
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


# TODO: index DB by username
# Get hash of user pass from DB
def get_user_pass_db(sql_cursor, username):
    
    # Because SQL conenctor wants tuples
    user_name = (username,)
    get_query = "SELECT passwd FROM users WHERE username = %s"
    sql_cursor.execute(get_query, user_name)
    user_pass = sql_cursor.fetchone()
    if (user_pass):
        return user_pass[0]
    else:
        return None

# Todo handle properly rendering error / redirect to home in caller?
def try_login_user(sql_cursor, username, pass_input):

    # return "adghajkegkl"
    pass_hash = get_user_pass_db(sql_cursor, username)
    if (pass_hash == pass_input):
        # return "Login success."
        return True
        # DO redirect to homepage here with logged in parameter
    else:
        # return "Login failed. pass mismtach: {} != {}".format(pass_input, pass_hash)
        return False
        # do redirect to login again with login failed

def create_log(id, username, door_id):
    time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    stamp = "Date & Time: {}, ID: {}, Username: {}, Door ID: {}".format(time, id, username, door_id)

    #     when utilising this function, make sure to import logging and include the bottom function within the file that you are logging for
    #     logging.basicConfig(filename='<filename>.log', level=logging.INFO)

    logging.info(stamp)
