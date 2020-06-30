import random
from audio import Audio

class circlegen():
    def __init__(self):
        print("todo")

    @staticmethod
    def getcircle(prevCircle=None):
        if prevCircle is None:
            # generate random safe circle
            return [random.randint(0, 640), random.randint(0, 480), random.randint(1, 20)]
        else:
            # generate entropy via movement
            if prevCircle[0] > 10 and random.randint(0, 1) != 0:
                prevCircle[0] = prevCircle[0] - 10
            if prevCircle[0] < 630 and random.randint(0, 1) != 0:
                prevCircle[0] = prevCircle[0] + 10
            if prevCircle[1] > 10 and random.randint(0, 1) != 0:
                prevCircle[1] = prevCircle[0] - 10
            if prevCircle[1] < 470 and random.randint(0, 1) != 0:
                prevCircle[1] = prevCircle[0] + 10
        return prevCircle

    @staticmethod
    def getcirclespin(prevCircle=None):
        if prevCircle is None:
            # generate random safe circle
            return [random.randint(0, 640), random.randint(0, 480), random.randint(1, 20)]
        else:
            # generate entropy via movement
            if prevCircle[0] % 10 == 0:
                # rising
                if  prevCircle[0] < 630:
                    # safe
                    prevCircle[0] = prevCircle[0] + 10
                else:
                    # flag turnaround
                    prevCircle[0] = 635
            if prevCircle[0] % 10 != 0:
                # falling
                if prevCircle[0] > 10:
                    prevCircle[0] = prevCircle[0] - 10
                else:
                    prevCircle[0] = 0

            if prevCircle[1] > 10 and random.randint(0, 1) != 0:
                prevCircle[1] = prevCircle[0] - 10
            if prevCircle[1] < 470 and random.randint(0, 1) != 0:
                prevCircle[1] = prevCircle[0] + 10
        return prevCircle


if __name__ == "__main__":
    pre = [0, 0]
    au = Audio([640, 480])
    while True:
        pre = circlegen.getcirclespin(pre)
        print(pre)
        au.generate1(pre)
