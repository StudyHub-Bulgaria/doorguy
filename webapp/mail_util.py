#!/user/bin/python

## This contains are mail sending API
import smtplib
from utils import DUser

# Send a mail to customer that their regitration was successful
def notify_user_reg_success(user_name):
    # Todo grab actual user email
    # Todo create user class to hold info in memory
    user_info = get_user_subscription_info(user_name)
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
    info = get_user_subscription_info(user_name)
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

    info = get_user_subscription_info(user_name)
    recepient = "info@studyhub.bg"
    recepient = "mail_info@studyhub.bg"

    # Add generic Person has registered
    # add info to email
    # send out with smtp to info@studyhub.bg

    # Add hook to call discord bot to notify channel

    return True


def send_smtp_mail(user_obj):
    sender = 'stub-master@localhost'
    hub_name = "StudyHub Team"
    receivers = user_obj.email

    message = """From: From {}
    To: {} <{}>
    Subject: SMTP e-mail test

    This is a test e-mail message.
    """.format(hub_name, user_obj.real_name, user_obj.email)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)         
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")


kon = DUser()
kon.real_name = "Johnny Do be good"
kon.email = "stub-master@firemint"

print("Sending mail to {} at {}".format(kon.real_name, kon.email))

send_smtp_mail(kon)