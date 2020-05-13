"""
Audio.py is responsible for generating audio feedback from processed
images/video-feed.

"""
from pydub.generators import Sine
from pydub import AudioSegment
from pydub.playback import play

class Audio:
    center_freq = 440 # A4 on a keyboard

    def __init__(self, dims):
        self.dims = dims
        self.sine_generator = Sine(self.center_freq)
        self.sine_tone = self.sine_generator.to_audio_segment(5, volume=-999999)
        self.sine_tone = self.sine_tone + self.sine_generator.to_audio_segment(50)
    
    def generate1(self, circle):
        # circle is [int, int, int] = [x, y, r]
        self.generate(circle, self.dims)
    
    def generate(self, circle, dimensions):
        """
        circle is a list of (x, y, r) ?votes
        dimensions is a list of (x, y)
        """
        # sine_generator= Sine(self.center_freq)
        # sine_tone = sine_generator.to_audio_segment(50)
        if circle[0] > dimensions[0] / 2 + 10:
            # target is on the right side of vision
            # TODO: make this parabolic / aka more aggressive panning
            play(self.sine_tone.pan(+(circle[0] / dimensions[0])))
        elif circle[0] < dimensions[0] / 2 - 10:
            # target is on left side of vision
            # TODO: make this parabolic / aka more aggressive panning
            play(self.sine_tone.pan(-((dimensions[0] - circle[0]) / dimensions[0])))
        else:
            play(self.sine_tone)

if __name__ == "__main__":
    au = Audio([640, 480])
    curIter = 10
    curCircle = [220, 240]
    while(True):
        print(curCircle)
        au.generate(curCircle, [640, 480])
        au.generate(curCircle, [640, 480])
        if curCircle[0] > 630 or curCircle[0] < 10:
            curIter = -curIter
        curCircle[0] += curIter
