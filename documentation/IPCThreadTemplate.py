#!/usr/bin/python

import time

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import IPCThread
IPCThread = IPCThread.Class

import DynamicObject
DynamicObject = DynamicObject.Class

# put your vars here

class Class (IPCThread):

    def __init__(self, name, API):
        IPCThread.__init__(self, name, API)

        self.registerOutput("audio", {"playing": False}) # providing default value makes dependants more stable. takes in any dictionary object or another DynamicObject

    def run(self):
        while 1:
            time.sleep(0.1)
            servo = self.getInputs().servo # inputs are a clone of outputs, so modifying this does not affect the real values
            playing = False
            if (servo.moving): playing = True
            self.output("audio", {"playing": playing}) # output any dictionary object or DynamicObject

