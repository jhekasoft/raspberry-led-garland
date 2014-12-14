import RPi.GPIO as GPIO

class GarlandEffect(object):
    delay = 1.0
    ledstate = 0

    def __init__(self, garland):
        self.garland = garland
        self.ledstate = 1

    def iterate(self):
        if not self.garland.checkIterationDelay(self.delay):
            return False

        self.garland.setLedsState(self.ledstate)
        self.garland.gpioOutSetState()
        self.ledstate = 1 - self.ledstate

        return True
