
SUBSCRIPTION_EPXIRE_DATE_Q = """SELECT validity_end from customer_subscriptions WHERE customer_id = %s """
CREATE_CUSTOMER_Q = """INSERT INTO customers (university, first_name, phone, zkteco_id, email) VALUES (%s, %s, %s,%s, %s); """
SELECT_CUSTOMER_ID_BY_USERNAME_Q = """SELECT customer_id FROM customer_accounts WHERE username = %s"""