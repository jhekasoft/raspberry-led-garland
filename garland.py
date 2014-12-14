import RPi.GPIO as GPIO
import time
import random
import sys
from effects import *

class Garland(object):
    leds = []
    button = {}
    effects = []
    currentEffect = ''

    def __init__(self, leds, button, effects):
        GPIO.setmode(GPIO.BOARD)

        self.leds = leds
        self.button = button
        self.effects = effects
        self.currentEffect = self.effects[0]

        GPIO.setup(self.button['num'], GPIO.IN)
        for led in self.leds:
            GPIO.setup(led['num'], GPIO.OUT)

    def setLedsState(self, state):
        for led in self.leds:
            led['state'] = state

    def gpioOutSetState(self):
        for led in self.leds:
            GPIO.output(led['num'], led['state'])

    def gpioLedsOff(self):
        self.setLedsState(0)
        self.gpioOutSetState()

    def gpioCleanup(self):
        self.gpioLedsOff()
        GPIO.cleanup()

    def getCurrentEffect(self):
        print("Set effect: %s" % self.currentEffect)
        return self.currentEffect

    def getNextEffect(self):
        currentEffectIndex = self.effects.index(self.currentEffect)
        nextEffectIndex = currentEffectIndex + 1
        if nextEffectIndex >= len(self.effects):
            nextEffectIndex = 0;
        self.currentEffect = self.effects[nextEffectIndex]

        return self.getCurrentEffect()

if __name__ == '__main__':
    try:
        garland = Garland(
            [{'num': 8, 'state': 0}, {'num': 11, 'state': 0}, {'num': 12, 'state': 0}, {'num': 13, 'state': 0}, {'num': 15, 'state': 0}, {'num': 16, 'state': 0}],
            {'num': 5},
            ['static', 'blink', 'run', 'off']
        )

        garland.gpioLedsOff()

        # effect init
        #effect = effects.blink.GarlandEffect(garland)
        effect = globals()[garland.getCurrentEffect()].GarlandEffect(garland)

        #while GPIO.input(garland.button['num']):
        while 1:
            # effect iteration
            effect.iterate()

            if GPIO.input(garland.button['num']) == False:
                garland.gpioLedsOff()
                effect = globals()[garland.getNextEffect()].GarlandEffect(garland)

        garland.gpioCleanup()

    except KeyboardInterrupt:
        garland.gpioCleanup()
