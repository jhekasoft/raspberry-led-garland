import RPi.GPIO as GPIO

class GarlandEffect(object):

    def __init__(self, garland):
        self.garland = garland
        self.garland.setLedsState(1)
        self.garland.gpioOutSetState()
 
    def iterate(self):
        pass
