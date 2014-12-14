import time
import RPi.GPIO as GPIO

class GarlandEffect(object):
    delay = 1.0
    ledstate = 0

    def __init__(self, garland):
        self.garland = garland
        self.ledstate = 1

    def iterate(self):
        self.garland.setLedsState(self.ledstate)
        self.garland.gpioOutSetState()
        time.sleep(self.delay)
        self.ledstate = 1 - self.ledstate
