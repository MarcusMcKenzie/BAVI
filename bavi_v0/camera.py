import cv2
import copy
import argparse
import os
import numpy as np
import math
from PIL import Image
import time
from audio import Audio
import imutils

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    REMOTE = True
except:
    REMOTE = False

print(REMOTE)
class Camera:
    args = None
    capture = None
    camera = None


##################################################################################
###################################### SETUP #####################################
##################################################################################
    def __init__(self, audio=None):
        global REMOTE
        self.au = audio
        self.args = self.parse_arguments()
        self.dims = [640, 480]
        if self.args["image"] is not None:
            self.test_image()
        if REMOTE: # when running on the pi
            self.camera = PiCamera()
            self.camera.resolution = (self.dims[0], self.dims[1])
            self.camera.framerate = 32
            self.rawCapture = PiRGBArray(self.camera, size=(self.dims[0], self.dims[1]))
            time.sleep(0.1)
            self.run()
        else: # when testing on a local machine
            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
            self.capture.set(3, 640)
            self.capture.set(4, 480)
            self.run()
        cv2.destroyAllWindows()
        exit(0)
    
    def parse_arguments(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-s", "--silent", action='store_true', help="no show images")
        ap.add_argument("-d", action='store_true', help = "debug mode")
        ap.add_argument("-i", "--image", help = "path to the image")
        ap.add_argument("-g", "--greedy", action="store_true", help = "greedy circle discard")
        return vars(ap.parse_args())

##################################################################################
###################################### TEST ######################################
##################################################################################
    
    def test_image(self):
        imagePath = self.args["image"]
        frame = cv2.imread(imagePath)

        res = self.hsv_proc(frame)
        res = self.circle_proc(res)
        cv2.imshow('res',res)

        cv2.waitKey(0)
    
    def supress(self, x, fs):
        for f in fs:
                distx = f.pt[0] - x.pt[0]
                disty = f.pt[1] - x.pt[1]
                dist = math.sqrt(distx*distx + disty*disty)
                if (f.size > x.size) and (dist<f.size/2):
                        return True

##################################################################################
################################### IMAGE OPS  ###################################
##################################################################################

    def blob_proc(self, img):
        # don't use me, im bad
        d_red = cv2.RGB(150, 55, 65)
        l_red = cv2.RGB(250, 200, 200)
        
        detector = cv2.FeatureDetector_create('MSER')
        fs = detector.detect(img)
        fs.sort(key = lambda x: -x.size)

        sfs = [x for x in fs if not self.supress(x, fs)]

        for f in sfs:
            cv2.circle(img, (int(f.pt[0]), int(f.pt[1])), int(f.size/2), d_red, 2, cv2.CV_AA)
            cv2.circle(img, (int(f.pt[0]), int(f.pt[1])), int(f.size/2), l_red, 1, cv2.CV_AA)
        
        h, w = orig.shape[:2]
        vis = np.zeros((h, w*2+5), np.uint8)
        vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
        vis[:h, :w] = orig
        vis[:h, w+5:w*2+5] = img

        return vis
        
    
    def circle_proc(self, img):
        # primary circle classiier
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=2.0)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2.0, 
              minDist=120,
              param1=80,
              param2=80,
              minRadius=0,
              maxRadius=40)
        # circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.0)
        # ensure at least some circles were found
        if circles is not None:
            # CIRCLES ARE OF DATA [[[x, y, r]]]
            # convert the (x, y) coordinates and radius of the circles to integers
            if self.args["greedy"]:
                bestCircle = self.discardWorst(circles)
                # draw the outer circle
                cv2.circle(img,(bestCircle[0],bestCircle[1]),bestCircle[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(img,(bestCircle[0],bestCircle[1]),2,(0,0,255),3)
#                self.au.generate(bestCircle, [640, 480])
                print(bestCircle)
                return img, bestCircle
            else:
                circles = np.uint16(np.around(circles))
                for i in circles[0,:]:
                    # draw the outer circle
                    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
                    # draw the center of the circle
                    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
                return img, circles
        else:
            return None, None

    def discardWorst(self, circles):
        circles = circles[0]
        bestHeur = 9999999999
        bestCircle = None
        for circle in circles:
            curHeur = abs(circle[0] - (self.dims[0]/2)) + abs(circle[1] - (self.dims[1]/2))
            if curHeur < bestHeur:
                bestCircle = circle
                bestHeur = curHeur
        return bestCircle

    def edge_proc(self, img):
        # don't user me, im bad
        img = cv2.Canny(img,200,200)
        return img
    
    def hsv_proc(self, img):
        # COLOR STRIPPER
        # https://stackoverflow.com/a/22588643
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # define range of white color in HSV
        # change it according to your need !
        sensitivity = 30
        lower_white = np.array([0,0,255-sensitivity])
        upper_white = np.array([255,sensitivity,255])

        # lower_red = np.array([30,150,50])
        # upper_red = np.array([255,255,180])

        # H: 0 - 180, S: 0 - 255, V: 0 - 255

        # RED
        lower_red = np.array([0, 140, 120])
        upper_red = np.array([15, 255, 255])
        lower_red_ = np.array([170, 140, 120])
        upper_red_ = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv, lower_red, upper_red)
        red_mask_ = cv2.inRange(hsv, lower_red_, upper_red_)
        
        # BLUE
        lower_blue = np.array([90, 40, 50])
        upper_blue = np.array([140, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # YELLOW
        lower_yellow = np.array([18, 80, 80])
        # upper_yellow = np.array([35, 255, 255])
        upper_yellow = np.array([35, 240, 200])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # BLACK
        # lower_black = np.array([0, 0, 0])
        # upper_black = np.array([180, 10, 10])
        # black_mask = cv2.inRange(hsv, lower_black, upper_black)

        #GREEN
        lower_green = np.array([50, 40, 50])
        upper_green = np.array([80, 180, 180])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)

        # Threshold the HSV image to get only white colors
        # Bitwise-AND mask and original image
        # return cv2.cvtColor(cv2.bitwise_and(img,img, mask= mask), cv2.COLOR_HSV2BGR)

        red = cv2.bitwise_or(cv2.bitwise_and(img,img, mask=red_mask), cv2.bitwise_and(img, img, mask=red_mask_))
        blue = cv2.bitwise_and(img, img, mask=blue_mask)
        yellow = cv2.bitwise_and(img, img, mask=yellow_mask)
        green = cv2.bitwise_and(img, img, mask = green_mask)
        # black = cv2.bitwise_and(img, img, mask=black_mask)

        # return cv2.bitwise_or(red, blue)
        acc = cv2.bitwise_or(red, blue)
        # acc = cv2.bitwise_or(cv2.bitwise_not(black), acc)
        return cv2.bitwise_or(red, green)

##################################################################################
################################ MAIN CONTROLLERS ################################
##################################################################################
    
    def run(self):
        global REMOTE
        # for both pi and local testing
        i = 0
        if REMOTE:
            # capture frames from the camera
            for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                image = imutils.rotate(image, 270)
#                image = cv2.flip(image, 1)
#                image = cv2.flip(image, 0)

                print("framedone") 
                image = self.hsv_proc(image)
                image = cv2.GaussianBlur(image, (5, 5), 0)
 #               image = self.circle_proc(image)

                try:
                    cv2.imshow("Frame", image)
                except:
                    pass
                key = cv2.waitKey(1) & 0xFF
            
                self.rawCapture.truncate(0)
            
                if key == ord("q"):
                    break
                i += 1
        else:
            while (self.capture.isOpened()):
                ret, frame = self.get_frame()
                if ret is True:
                    try:
                        frame = self.hsv_proc(frame)
                        #frame = cv2.GaussianBlur(frame,(5,5), 0)
                        frame, circles = self.circle_proc(frame)
                        cv2.imshow('Frame', frame)
                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                    except:
                        pass
                
    
    def one_frame(self, i):
        global REMOTE
        # do all image operations here
        ret, frame = self.get_frame()
        # fps = self.capture.get(cv2.CAP_PROP_FPS)
        # print("FPS : {0}".format(fps))
        if ret == True:
            frame = imutils.rotate(frame, 90)
            try:
                frame = self.hsv_proc(frame)
                frame = cv2.GaussianBlur(frame,(5,5), 0)

                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # frame = cv2.blur(frame,(5,5))
                # retval, frame = cv2.threshold(frame, 40, 255, cv2.THRESH_TOZERO)

                # frame = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
                # frame = self.edge_proc(frame)
                # frame = self.blob_proc(frame)
                # frame = cv2.GaussianBlur(frame,(10,10), 0)

                frame, circles = self.circle_proc(frame)
                if REMOTE:
                    remote_frame = Image.fromarray(frame, 'RGB')
                    remote_frame.show()
                    print("shown ^^^")
                else:
                    cv2.imshow('Frame', frame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        return True
                if self.args["d"]:
                    self.save_image(frame, "raw", i)
            except:
                pass
    
##################################################################################
################################# IMAGE CAPTURE ##################################
##################################################################################
    
    def get_frame(self):
        global REMOTE
        if REMOTE:
            self.camera.capture(self.capture, format="bgr")
            return True, self.capture.array
        else:
            ret, frame = self.capture.read()
            resized = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_AREA)
            return ret, resized
    
    def save_image(self, frame, prefix, idx):
        cv2.imwrite(str(os.path.abspath(os.getcwd())) + '/dump/' + str(prefix) + '_' + str(idx) + '.png', frame)


if __name__ == "__main__":
    au = Audio([640, 480])
    cam = Camera(au)
