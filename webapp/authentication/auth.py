### This files will check user UIDs against the DB and return an acept / deny to the door controller ###

import hashlib
import mysql.connector


# read credentials file for local copy of DB
def get_local_db_creds():

    # TODO: move creds to external file
    creds = ("localhost", "read_tester", "test_pass", "studyhub_portal_users")
    return creds

#    with open("local_credentials") as creds_file:
#        raw_text = creds_file.read()
#        creds = raw_text.split(";")

# try to authenticate the hash read from user QR against the DB
# Key will probably be sha256
# TBD: do we want to rotate keys on login  / say 20 min timeout on login session or keep them the same for a user until something happens?
# if rotate, do we keep a pool of keys to reuse or regenerate new SHA key (user_secret + time_thing)? -> if internet / somethin breaks along the way, user cant
# go in / go out :( update server, DP, hosted DB, phone, maybe local door thing?

# maybe keep old keys just for checking?

def check_user_local_db(user_hash):
    login_db()

    # Keep all our shit in a separate table and use JOIN() magic to grab names from other table
    query = "SELECT user_id, first_name, user_key, validity FROM portal_users WHERE user_key = %s";
    #cursor.execute(query, user_key)

    # INCORRECT, SECURITY ISSUE
    # c.execute("SELECT * FROM foo WHERE bar = %s AND baz = %s" % (param1, param2))

    # CORRECT, with ESCAPING
    # c.execute("SELECT * FROM foo WHERE bar = %s AND baz = %s", (param1, param2))

    # run query

    # user_key = query_result{"user_key"}
    user_key = "cherno_i_bqlo"

    # something = cursor.fetchrow()
    # if (something == "NULL" ) # or empty row, whatever the syntax

    # THO during normal operation we should not get this, unless QR read was bad, because if they have a QR, they should be valid? where do we handle that
    # -> TDB
    # print errors / warnings

def login_db():

    creds = get_local_db_creds()

    db_host = creds[0]
    db_user = creds[1]
    db_pass = creds[2]
    db_name = creds[3]


    # debug prints
    print("[debug] Connecting to db on host: {}".format(db_host))
    print("[debug] database name: {}".format(db_name))
    print("[debug] username: {}".format(db_user))
    print("[debug] clear pass: {}".format(db_pass_clear))

    # mysql.connector bla bla

login_db()
