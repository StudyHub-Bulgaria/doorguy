import mysql.connector

# This file contains our sql functions and queres

def create_user(sql_cursor, username, passwd,uuid): 
    
    # Maybe generate uuid here?
    # generate_user_uuid(username,pass, personal_info)
    # validate_credentials()

    create_query = "INSERT INTO users (username, web_passwd, UUID_hash) VALUES (%s,%s,%s)"
    user_data = ("john_doe", "parola123", "azobichamazis")
    
    sql_cursor.execute(create_query, user_data)
    print("about to call {}".format(create_query))
    # sql_cursor.execute(create_query)
    # print("created user")
    


def insert_user_uuid():
    s = 30


# def insert_query(): # adds base64 from qr code
#     qrGen.generate(info)
#     base64_string = qrGen.decode_base64()

#     query = ("INSERT INTO test (test_field) VALUES ('{}')".format(base64_string))
#     print (query)
#     cursor.execute(query)

# insert_query() ## does not insert for some reason, although no errors are present

# cursor.close()
# cnx.close()


# conn, conn_cursor = connect_db()
# create_user(conn_cursor)
