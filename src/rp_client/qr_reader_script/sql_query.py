import qr_code_generator as qrGen
import mysql.connector

# This file is going to insert SQL data that contains user information.
# The hardcoded is going to be dynamic. The user information is going to
# be contained within the QR code

info = 'pesheca' #dynamic info --> depends on who is the user using the login function

cnx = mysql.connector.connect(
    user="root",
    password="",
    host="localhost",
    database="qr")
cursor = cnx.cursor()

def test_query(): # debugging purposes
    query = ("SELECT * FROM test")
    cursor.execute(query)

    for item in cursor:
        print(item)

def insert_query(): # adds base64 from qr code
    qrGen.generate(info)
    base64_string = qrGen.decode_base64()

    query = ("INSERT INTO test (test_field) VALUES ('{}')".format(base64_string))
    print (query)
    cursor.execute(query)

insert_query() ## does not insert for some reason, although no errors are present

cursor.close()
cnx.close()
