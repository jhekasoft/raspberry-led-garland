import time
import RPi.GPIO as GPIO

class GarlandEffect:
    ledscount = 0
    currentLedNum = 0

    def __init__(self, garland):
        self.garland = garland
        self.ledscount = len(self.garland.leds)
        self.currentLedNum = 0

    def iterate(self):
        self.garland.gpioOutSetState()
        time.sleep(1)
        for led in self.garland.leds:
            if self.garland.leds.index(led) == self.currentLedNum:
                led['state'] = 1
            else:
                led['state'] = 0
        self.currentLedNum += 1
        if self.currentLedNum >= self.ledscount:
            self.currentLedNum = 0
