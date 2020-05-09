import cv2
import copy
import argparse
import os
import numpy as np
import math
from PIL import Image
import time
import imutils
import datetime
import pyaudio

def discard_worst(circles):
        circles = circles[0]
        bestHeur = 9999999999
        bestCircle = None
        for circle in circles:
            curHeur = abs(circle[0] - (320)) + abs(circle[1] - (240))
            if curHeur < bestHeur:
                bestCircle = circle
                bestHeur = curHeur
        return bestCircle

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())
# img = cv2.imread(args["image"],0)
img = cv2.imread(args["image"], cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
# img = cv2.resize(img, (640, 480))
# img = cv2.medianBlur(img,5)
# ret, img = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
#ret, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
# img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
# cimg = cv2.GaussianBlur(img,(5,5), 0)
# frame = img
# hsv = frame
# frame = img
frame = img
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_green = np.array([40, 100, 105])
upper_green = np.array([90, 255, 255])
green_mask = cv2.inRange(hsv, lower_green, upper_green)
# img = cv2.bitwise_and(frame, frame, mask=green_mask)
# img = cv2.GaussianBlur(img,(5,5), 0)

frame = img
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2.0, 
        minDist=120,
        param1=20,#80,
        param2=40,#80,
        minRadius=0,
        maxRadius=40)
              
bestCircle = discard_worst(circles)
print(str(bestCircle))
# cv2.circle(img,(bestCircle[0],bestCircle[1]),bestCircle[2],(0,255,0),2)
# cv2.circle(img,(bestCircle[0],bestCircle[1]),2,(0,0,255),3)


# circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,319,
#                             param1=100,param2=30,minRadius=0,maxRadius=0)

# circles = np.uint16(np.around(circles))
# for i in circles[0,:]:
#     # draw the outer circle
#     cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#     # draw the center of the circle
#     cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
