import time
import RPi.GPIO as GPIO

class GarlandEffect(object):
    delay = 1.0
    ledscount = 0
    currentLedIndex = 0

    def __init__(self, garland):
        self.garland = garland
        self.ledscount = len(self.garland.leds)
        self.currentLedIndex = 0

    def iterate(self):
        self.garland.gpioOutSetState()
        time.sleep(self.delay)
        for index, led in enumerate(self.garland.leds):
            if index == self.currentLedIndex:
                led['state'] = 1
            else:
                led['state'] = 0
        self.currentLedIndex += 1
        if self.currentLedIndex >= self.ledscount:
            self.currentLedIndex = 0
