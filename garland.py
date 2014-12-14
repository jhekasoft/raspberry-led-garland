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
import sys
import os
import signal
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

        self.gpioLedsOff()

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
    # Kill/keyboard interrupt signal handling
    def signal_handler(signal, frame):
        garland.gpioCleanup()
        sys.exit(0)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Loading config from JSON-file
    jsonSettingsData = open(os.path.dirname(os.path.realpath(__file__))+'/settings.json')
    settings = json.load(jsonSettingsData)

    # Garland init
    garland = Garland(settings['leds'], settings['button'], settings['effects'])

    # Effect init
    effect = globals()[garland.getCurrentEffect()].GarlandEffect(garland)

    while 1:
        # Effect iteration
        effect.iterate()

        # Button handling
        if GPIO.input(garland.button['num']) == False:
            garland.gpioLedsOff()
            effect = globals()[garland.getNextEffect()].GarlandEffect(garland)

    garland.gpioCleanup()
