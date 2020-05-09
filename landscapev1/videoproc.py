import argparse

"""
Flow:

at any point: if args.debug
    save intermediate processing?
    or just save final processed image?

init video capture
curFrame = cap.read()
if args.log_raw_video
    save curFrame - use this so we can test the saved videos later
blur?
process colors
    ? HSV color space ?
    auto-tune?
edge detection? probs nah
fill gaps? aka manual pixel based blurring?
can we then maybe try to find the biggest blob, and filter out everything else?
hough!
    process seems to be
    hough
    |> check # circles
    |> if # bad, re-hough
    |> else find concenctric coordinates, return best-center match
audio
    abs(coords - center) -> x,y audio feedback


"""

class videoProcessor:
    colorSpace = [
        ([0, 0, 0], [0, 0, 0])
    ]
    args = None

    def __init__(self):
        self.args = self.parseArguments()
    
    def parseArguments(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("--savecolor", action="store_true")
        ap.add_argument("--saveprocessed", action="store_true")
        ap.add_argument("--docolor", action="store_true")
        ap.add_argument("--docircle", action="store_true")
        return vars(ap.parse_args())
    
    def videoCapture(self, cap):
        # this needs to be 
        # https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                try:
                    outFrame = cv2.resize(outFrame, dsize=None, fx=0.4, fy=0.4) # resize
                    cv2.imshow('Frame',outFrame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
                except:
                    pass
            else: 
                break
        cap.release()
        cv2.destroyAllWindows()