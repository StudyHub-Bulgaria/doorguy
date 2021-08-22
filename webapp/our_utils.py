import mysql.connector
import re
import hashlib
from datetime import datetime
import logging

def escape_user_string(src):
    tmp = src
    re.sub('[^A-Za-z0-9]+', '', tmp)
    return tmp

def sha_wrap(src):
    return hashlib.sha512(src)
    
# TODO: move db creds to config file, change db creds to something legit
# Connect to DB and return cursor object - use once, pass cursor around!
def connect_db():

    # TODO Get DB credentials from safe file
    # read_credentials()
    cnx = mysql.connector.connect(
        user="dumble",
        password="",
        host="localhost",
        database="sh_portal")
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
