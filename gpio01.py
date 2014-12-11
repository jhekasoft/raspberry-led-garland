import RPi.GPIO as GPIO
import time
import random
import sys

GPIO.setmode(GPIO.BOARD)

led1 = 8 #7 #23
led2 = 11
led3 = 12
button = 5

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(button, GPIO.IN)

#GPIO.output(led1, 0)
#GPIO.output(led2, 0)
#GPIO.output(led3, 0)
#sys.exit()

GPIO.output(led1, 1)
GPIO.output(led2, 1)
GPIO.output(led3, 1)

time.sleep(1)
#time.sleep(random.uniform(5,10))
#GPIO.output(led, 0)

#while 1:
#    print ("%s", str(GPIO.input(button)))
#    time.sleep(0.01)

while GPIO.input(button):
    pass

if GPIO.input(button) == False:
    GPIO.output(led1, 0)
    GPIO.output(led2, 0)
    GPIO.output(led3, 0)
    print("Button pressed")

GPIO.cleanup()

