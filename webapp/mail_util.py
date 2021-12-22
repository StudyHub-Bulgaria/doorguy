## This contains are mail sending API

import smtplib
import utils

# Send a mail to customer that their regitration was successful
def notify_user_reg_success(user_name):
    # Todo grab actual user email
    # Todo create user class to hold info in memory
    user_info = get get_user_subscription_info(user_name)
    recepient = "test_user@domain.example"
    recepient = "mail_info@studyhub.bg"

    # Add generic Person has registered
    # add info to email
    # send out with smtp to info@studyhub.bg

    # Add hook to call discord bot to notify channel
    s = 30
    return True

# Send a mail to info@studyhub.bg that a customer has registered.
def notify_us_reg_success(user_name):
    info = get get_user_subscription_info(user_name)
    recepient = "info@studyhub.bg"
    recepient = "mail_info@studyhub.bg"

    # Add generic Person has registered
    # add info to email
    # send out with smtp to info@studyhub.bg

    # Add hook to call discord bot to notify channel
    return True

# Send a mail to customer that their payment is okay, subscribtion details
def notify_user_payment_okay(user_name):
    info = get_user_subscription_info(user_name)

    # Add generic Hello customer message
    # Add info to email
    # Sign
    # Send out with smtp
    return True

# Send a mail to info@studyhub that customer subscribtion is started
def notify_us_payment_success(user_name):

    info = get get_user_subscription_info(user_name)
    recepient = "info@studyhub.bg"
    recepient = "mail_info@studyhub.bg"

    # Add generic Person has registered
    # add info to email
    # send out with smtp to info@studyhub.bg

    # Add hook to call discord bot to notify channel

    return True