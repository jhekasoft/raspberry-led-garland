#!/usr/bin/env python
#title           :garland.py
#description     :LED garland driver.
#author          :jhekasoft
#date            :20141214
#version         :0.2
#usage           :python3 garland.py
#notes           :
#python_version  :3.4
#==============================================================================

import RPi.GPIO as GPIO
import time
import random
import sys
import os
import json
from effects import *

class Garland(object):
    leds = []
    button = {}
    effects = []
    currentEffectIndex = ''

    def __init__(self, leds, button, effects):
        GPIO.setmode(GPIO.BOARD)

        self.leds = leds
        self.button = button
        self.effects = effects
        self.currentEffectIndex = 0

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
        currentEffect = self.effects[self.currentEffectIndex]
        print("Set effect: %s" % currentEffect)
        return currentEffect

    def getNextEffect(self):
        nextEffectIndex = self.currentEffectIndex + 1
        if nextEffectIndex >= len(self.effects):
            nextEffectIndex = 0;
        self.currentEffectIndex = nextEffectIndex

        return self.getCurrentEffect()

if __name__ == '__main__':
    try:
        jsonSettingsData = open(os.path.dirname(os.path.realpath(__file__))+'/settings.json')
        settings = json.load(jsonSettingsData)

        garland = Garland(settings['leds'], settings['button'], settings['effects'])

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
