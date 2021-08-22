import cv2 as cv
import numpy as np
from pyzbar .pyzbar import decode


# This file turns on the camera and searches for a QR code, which it then reads (detects data from QR code only)

#img = cv.imread("qr.png") #image is now loaded in OpenCV
#qr_decoded = decode(img) #decodes pic that is 1d; displays everything about the QR code, incl position

#.data - just the data that the QR code has; data is converted to bytes
#.rect - information regarding the rectangle

# this next bit is if multiple QR codes will be displayed on the same picture

camera = cv.VideoCapture(0) # int is id for camera
camera.set(3,640) # 3 is for height
camera.set(4,480) # 4 is for width

while True:

    success, img = camera.read()
    for code in decode(img):

        decoded_data = code.data.decode("utf-8")
        print("QR scanner decoded: ",decoded_data)
        cv.waitKey(300)

    cv.imshow("Camera1 ",img)
    cv.waitKey(50) # delay of 800ms between readings 
