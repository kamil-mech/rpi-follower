#!/usr/bin/python

import time
import random

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import IPCThread
IPCThread = IPCThread.Class

import DynamicObject
DynamicObject = DynamicObject.Class

# import RPi.GPIO as GPIO
# GPIO.setwarnings(False)
#print " Values must be between -90 and 90"

# put your vars here


class Class (IPCThread):

    def __init__(self, name, API):
        IPCThread.__init__(self, name, API)

        self.registerOutput("test2", { "x": 0, "y": 0 })

    def run(self):
        while 1:
            self.output("test2", {"x": random.randint(-90, 90), "y": random.randint(-90, 90)})
            time.sleep(10)
