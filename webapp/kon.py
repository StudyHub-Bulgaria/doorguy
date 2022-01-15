import re


def validate_user_pass(usr_pass, re_pass):
    print("[debug] valdiating password: ", usr_pass)
    if (usr_pass != re_pass):
        return "Both password fields are required."
    quotes = re.match('[\'\"]', usr_pass)
    # if (quotes):
    #     print("matched quotes: ", quotes)
    # else:
    #     print("password does not contain quotes")
    return quotes

passin = "password,"
passin2 = "pass"

ret = validate_user_pass(passin, passin)
print(ret)
ret = validate_user_pass(passin, passin2)
print(ret)