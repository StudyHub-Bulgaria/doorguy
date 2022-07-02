
SUBSCRIPTION_EPXIRE_DATE_Q = """SELECT validity_end from customer_subscriptions WHERE customer_id = %s """
CREATE_CUSTOMER_Q = """INSERT INTO customers (university, first_name, phone, zkteco_id, email) VALUES (%s, %s, %s,%s, %s); """
SELECT_CUSTOMER_ID_BY_USERNAME_Q = """SELECT customer_id FROM customer_accounts WHERE username = %s"""
USER_HAS_SUBSRIPTION_Q = """SELECT active, validity_start, validity_end FROM customer_subscriptions WHERE customer_id = %s"""
SUBSCRIPTION_IS_VALID_Q = """"""

## Password related queries
CHANGE_USER_PASSWORD_Q = """UPDATE customer_accounts SET password = %s WHERE customer_id = %s"""
GET_USER_PASSWORD_Q = """SELECT password FROM customer_accounts WHERE customer_id = %s"""
GET_USER_QR_CODE_PATH_Q = """SELECT qr_path from customer_subscriptions WHERE customer_id = %s"""