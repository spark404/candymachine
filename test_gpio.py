#!/usr/bin/python

import RPi.GPIO as GPIO
import sys
import time

print "Activating GPIO %s" % sys.argv[1]

GPIO.setmode(GPIO.BCM)
        
GPIO.setup(int(sys.argv[1]), GPIO.OUT)
GPIO.output(int(sys.argv[1]), GPIO.HIGH)
try:
    time.sleep(300)
except KeyboardInterrupt:
    pass

GPIO.output(int(sys.argv[1]), GPIO.LOW)
GPIO.cleanup()


