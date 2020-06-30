from multiprocessing import Process
from pydub.generators import Sine
from pydub import AudioSegment
from pydub.playback import play
import time
import os
from copy import copy

class Audio2:
    center_freq = 440
    sine_generator = Sine(center_freq)
    duration = 100 # ms

    def __init__(self):
        print("todo")

    def generate(self, upTime=0, invert=False):
        upSound = self.sine_generator.to_audio_segment(upTime * self.duration, volume=0)
        downSound = self.sine_generator.to_audio_segment((1 - upTime) * self.duration, volume=-99999)
        # if invert:
            # return downSound + upSound + downSound + upSound + downSound + upSound + downSound + upSound + downSound + upSound + downSound + upSound
        # else:
        return upSound + downSound + upSound + downSound + upSound + downSound + upSound + downSound + upSound + downSound + upSound + downSound + upSound + downSound + upSound + downSound + upSound + downSound + upSound + downSound + upSound + downSound + upSound + downSound
    
    def go(self, sound):
        play(sound)
    
    def master(self, upTime=0, invert=False, pid=None):
        audio = self.generate(upTime, invert)
        play(audio)
        if pid is not None:
            print("KILLING " + str(pid))
            # time.sleep(1)
            os.kill(pid, 1)
            print("KILLED: " + str(pid))

if __name__ == "__main__":
    au = Audio2()
    curDir = +0.05
    curUpTime = 0.1
    pid = None
    while True:
        # do some shit
        curUpTime += curDir
        if curUpTime >= .95 and curDir > 0:
            curDir = 0 - curDir
        if curUpTime <= .15 and curDir < 0:
            curDir = 0 - curDir
        # au.master(curUpTime)
        p = Process(target=au.master, args=(curUpTime, False, pid))
        p.start()
        pid = copy(p.pid)
        time.sleep(0.5)

    # p0 = Process(target=au.master, args=(0.25, True, pid=None))
    # p1 = Process(target=au.master, args=(0.25, False))
    # # p3 = Process(target=au.master, args=(0.65, ))
    # p0.start()
    # p1.start()
    # # p2 = Process(target=au.master, args=(0.45, ))
    # print(p0.pid)
    # print(p1.pid)
    # # p2.start()
    # # p3.start()
    # p0.join()
    # p1.join()
    # # p2.join()
    # p3.join()