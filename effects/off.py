import RPi.GPIO as GPIO

class GarlandEffect(object):

    def __init__(self, garland):
        self.garland = garland
        self.garland.setLedsState(0)
        self.garland.gpioOutSetState()

    def iterate(self):
        pass
