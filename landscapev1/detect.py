import cv2
import numpy as np
import os
import argparse
import copy

"""
To run me:
python3 detect.py --imagedir some/directory/
    where some/directory contains images named like "img-#.xxx"
or if u only want to test one images (not batch mode)
python3 detect.py --image some_image.jpg
"""

class imageProcessor:
    """
    Defines the target colors to extract from 
    Need to gather test images to determine which colors are the most foriving
    In other words, we need to find out which colors we need as a minimum
    to get a reasonable true positive rate, while maintaining a low
    false positive rate.
    """
    colorSpace = [
        ([28, 28, 118], [96, 96, 255]), # DETECT RED
        ([100, 80, 0], [180, 140, 90]) # DETECT BLUE
        # ([0, 0, 0], [0, 0, 0]), # init
    ]

    def __init__(self):
        """
        Parse command line args, parse images or image directory accordingly
        This is where we would end up incorporating video stream as an option
        """
        args = self.parseArguments()
        self.args = args
        if args["imagedir"] is None and not args["v"]:
            self.master(self.loadImage(args["image"]))
        elif args["v"] is None and not args["v"]:
            for subdir in os.walk(os.path.join(os.getcwd(), args["imagedir"])):
                for thing in subdir[2]:
                    if "img-" in thing:
                        self.master(self.loadImage("img/pos/" + thing))
        else:
            cap = cv2.VideoCapture(0)
            if (cap.isOpened() == False): 
                print("Error opening video stream or file")
                exit(1)
            self.videoProc(cap)
        # else:
        #     cap = cv2.VideoCapture(0)
        #     if (cap.isOpened() == False): 
        #         print("Error opening video stream or file")
        #         exit(1)
        #     self.testColorSpaces(cap)
    
    def master(self, image):
        out = self.colorProc(image) # generate color filtered image
        out = self.circleProc(out)
        cv2.imshow("diff", np.hstack([image, out]))
        cv2.waitKey(0)
    
    def videoProc(self, cap):
        # https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
        while(cap.isOpened()):
            ret, frame = cap.read()
            frame_ = copy.deepcopy(frame)
            frame = self.colorProc(frame)
            outFrame = self.circleProc(frame, frame_)
            if ret == True:
                try:
                    outFrame = cv2.resize(outFrame, dsize=None, fx=0.4, fy=0.4)
                    cv2.imshow('Frame',outFrame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
                except:
                    pass
            else: 
                break
        cap.release()
        cv2.destroyAllWindows()
    
    def testColorSpaces(self, cap):
        # https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
        ii = 0
        while(cap.isOpened()):
            # if ii % 10 is 0:
            self.iterateColors()
            ret, frame = cap.read()
            frame_ = copy.deepcopy(frame)
            frame = self.colorProc(frame)
            # outFrame = self.circleProc(frame, frame_)
            if ret == True:
                try:
                    cv2.imshow('Frame',frame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
                except:
                    pass
            else: 
                break
            ii += 1
        cap.release()
        cv2.destroyAllWindows()
    
    def iterateColors(self):
        print(self.colorSpace)
        if self.colorSpace[0][1][2] < 255:
            self.colorSpace[0][1][2] += 1 # raise red ceiling
        else:
            self.colorSpace[0][0][2] += 1 # raise red floor
        print(self.colorSpace)

    def parseArguments(self):
        """
        Initialize argparse, process user arguments
        """
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", help = "Path to the image")
        ap.add_argument("-id", "--imagedir", help = "Path to the imagedir")
        ap.add_argument("-v", action='store_true', help = "video mode")
        ap.add_argument("-d", action='store_true', help = "debug mode")
        return vars(ap.parse_args())

    def loadImage(self, imagePath, zero=None):
        if zero is None:
            return cv2.imread(imagePath) # load img
        else:
            return cv2.imread(imagePath, 0) # load img
    
    def colorProc(self, image):
        """
        Iterate thru all target colors to extract
        TODO: finish me
        """
        curImg = None
        for colorVector in self.colorSpace:
            output = self.colorStrip(image, colorVector)
            if curImg is None:
                curImg = output
            else:
                curImg = curImg + output
        return curImg
    
    def colorStrip(self, image, bgrVals):
        """
        Receives an image and RGB array definition. Applies masking
        to image using bgrVals (if x,y pixel in image is in bgrVals range,
        keep it, else discard)
        :param image: image, expected result from self.loadImage(...)
        :param bgrVals: [[Bmin, Gmin, Rmin], [Bmax, Gmax, Rmax]] (0-255)
        :return: image
        """
        lower = np.array(bgrVals[0], dtype = "uint8")
        upper = np.array(bgrVals[1], dtype = "uint8")
        mask = cv2.inRange(image, lower, upper)
        return cv2.bitwise_and(image, image, mask = mask)
    
    def circleProc(self, image, ogFrame=None):
        """
        TODO: this is literal garbage
        ripped from https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
        """
        # detect circles in the image
        output = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if ogFrame is None:
            ogFrame = output

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=2.0, minDist=240, param1=400, param2=130, minRadius=0, maxRadius=180)
        # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=2.0, minDist=240, param1=400, param2=200, minRadius=0, maxRadius=180)
        # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=2.0, minDist=20, param1=300, param2=15, minRadius=0, maxRadius=0)
        
        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
        
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        
            return output
            # show the output image
            # if self.args["d"] is False:
            #     return output
            # return output   
        else:
            print("no circles")
            return None

if __name__ == "__main__":
    lol = imageProcessor()