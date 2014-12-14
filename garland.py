#!/usr/bin/env python

__author__     = "Evgeniy Efremov"
__copyright__  = "Copyright 2014, jhekasoft"
__credits__    = ["Evgeniy Efremov"]
__license__    = "GPL"
__version__    = "0.3"
__maintainer__ = "Evgeniy Efremov"
__email__      = "jheka@mail.ru"

import RPi.GPIO as GPIO
import time
import sys
import os
import signal
import logging
import json
from effects import *

class Garland(object):
    leds = []
    button = {}
    effects = []
    currentEffectIndex = ''
    iterationDelay = 0.05
    previousIterationTimestamp = 0
    previousButtonState = 0

    def __init__(self, leds, button, effects, logger = None):
        self.logger = logger

        # Logging
        if (self.logger):
            self.logger.info("Started")

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

        # Logging
        if (self.logger):
            self.logger.info("Ended")

    def getCurrentEffect(self):
        currentEffect = self.effects[self.currentEffectIndex]

        # Logging
        if (self.logger):
            self.logger.info("Set effect: %s" % currentEffect)

        return currentEffect

    def gotoNextEffect(self):
        nextEffectIndex = self.currentEffectIndex + 1
        if nextEffectIndex >= len(self.effects):
            nextEffectIndex = 0;
        self.currentEffectIndex = nextEffectIndex

        return self.getCurrentEffect()

    def changeIterationTimestamp(self):
        self.previousIterationTimestamp = time.time()

    def checkIterationDelay(self, delay):
        if self.previousIterationTimestamp + delay <= time.time():
            return True

        return False

    def isButtonWasPressed(self):
        if not GPIO.input(self.button['num']) and self.previousButtonState == 0:
            self.previousButtonState = 1

            # Logging
            if (self.logger):
                self.logger.info("Ended")

            return True;
        elif GPIO.input(self.button['num']) and self.previousButtonState == 1:
            self.previousButtonState = 0

        return False;

    def resetIterationTimestamp(self):
        self.previousIterationTimestamp = 0

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

    # Logger
    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(settings['logfile'])
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Garland init
    garland = Garland(settings['leds'], settings['button'], settings['effects'], logger)

    # Effect init
    effect = globals()[garland.getCurrentEffect()].GarlandEffect(garland)

    while 1:
        # Effect iteration
        if effect.iterate():
            effect.garland.changeIterationTimestamp()
        time.sleep(effect.garland.iterationDelay)

        # Button handling
        if effect.garland.isButtonWasPressed():
            garland.gpioLedsOff()
            garland.resetIterationTimestamp()
            effect = globals()[garland.gotoNextEffect()].GarlandEffect(garland)

    garland.gpioCleanup()
