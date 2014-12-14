import time
import RPi.GPIO as GPIO

class GarlandEffect:

    def __init__(self, garland):
        self.garland = garland
        self.garland.setLedsState(0)
        self.garland.gpioOutSetState()
 
    def iterate(self):
        time.sleep(1)
