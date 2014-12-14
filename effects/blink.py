import time
import RPi.GPIO as GPIO

class GarlandEffect:
    ledstate = 0

    def __init__(self, garland):
        self.garland = garland
        self.ledstate = 1

    def iterate(self):
        self.garland.setLedsState(self.ledstate)
        self.garland.gpioOutSetState()
        time.sleep(1)
        self.ledstate = 1 - self.ledstate
