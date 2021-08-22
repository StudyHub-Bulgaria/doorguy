import numpy as np
from pyzbar .pyzbar import decode
from PIL import Image
import qrcode
import base64

# This file generates a QR code png. The QR code can be adjusted by changing the code

#    version — Accepts an integer from 1 to 40 which controls the size of the QR Code. The smallest version 1 has a dimension of 21 x 21.
#    box_size — Determines the number of pixels for each box of the QR code.
#    border — Determines the thickness of the border of the boxes. The default value is 4, which is the minimum size.
#    error_correction — Controls the error correction used. It will be further explained in the next paragraph.

    #    ERROR_CORRECT_L — About 7% or fewer errors can be corrected.
    #    ERROR_CORRECT_M — About 15% or fewer errors can be corrected. This is the default value.
    #    ERROR_CORRECT_Q — About 25% or fewer errors can be corrected.
    #    ERROR_CORRECT_H — About 30% or fewer errors can be corrected.

def generate(name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(name)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    img.save('QR_code.png')

def decode_base64():
    path = r'D:\xampp\htdocs\hub-portal\QR Reader script\QR_code.png'

    with open("QR_code.png","rb") as qr_image:
        b64string = base64.b64encode(qr_image.read())

    return b64string.decode('utf-8') # when converting into base64, there is a b char in the beggining. this removes it
