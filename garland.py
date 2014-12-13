import RPi.GPIO as GPIO
import time
import random
import sys

GPIO.setmode(GPIO.BOARD)
leds = [8, 11, 12, 13, 15, 16]
button = 5
ledstate = 1

GPIO.setup(button, GPIO.IN)
for led in leds:
    GPIO.setup(led, GPIO.OUT)

while GPIO.input(button):
    time.sleep(0.1)
    ledstate = 1 - ledstate
    print("state: %d" % ledstate)
    for led in leds:
        GPIO.output(led, ledstate)

if GPIO.input(button) == False:
    print("Button pressed")

for led in leds:
    GPIO.output(led, 0)
GPIO.cleanup()
