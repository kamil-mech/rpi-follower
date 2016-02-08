#!/usr/bin/python

# import from modules directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "/modules")

import threading
import time
import copy

import DynamicObject
DynamicObject = DynamicObject.Class

MsgLock = threading.RLock()
IOLock = threading.RLock()

# enable / disable messages
logComms = False
if (len(sys.argv) > 1 and sys.argv[1] == '-debug'): logComms = True

threads = {}
comms = DynamicObject({})

# load modules here
import OpenCV
OpenCV = OpenCV.Class
import Servo
Servo = Servo.Class
import Audio
Audio = Audio.Class

def registerOutput (owner, tag, default):
    with MsgLock:
        if (comms[tag] and comms[tag].owner != owner):
            return printSync("WARNING: Cannot register tag '{}'. Already registered by thread '{}'.".format(tag, comms[tag].owner.name))
        
        default = DynamicObject(default)
        print("Registered '{}' tag with owner thread '{}' and default output '{}'.".format(tag, owner.name, default))
        default.owner = owner
        comms[tag] = default

def output (thread, tag, value):
    with MsgLock:
        if (comms[tag].owner != thread):
            return printSync("WARNING: '{}' cannot output with '{}' tag. ACCESS DENIED. Thread '{}' has tag ownership.".format(thread.name, tag, comms[tag].owner.name))
        comms[tag].extend(value)
        info = copy.copy(comms[tag])
        del info.owner
        if (logComms): print(" OUTPUT by {}: [{} tag] {}".format(thread.name, tag, info))

def getInputs ():
    with MsgLock:
        return copy.copy(comms)

def printSync (msg):
    with IOLock:
        print(msg)

def message (thread, msg):
    printSync("MESSAGE by {}: {}".format(thread.name, msg))

def addThread (Class, name):
    API = {
        "registerOutput": registerOutput,
        "getInputs": getInputs,
        "output": output,
        "message": message
    }
    threads[name] = Class(name, API)

# Create threads
addThread(OpenCV, "opencv")
addThread(Servo, "servo")
addThread(Audio, "audio")

# Start threads
for t in threads:
    threads[t].daemon = True # make sure threads close with main thread
    threads[t].start()

# make sure main thread dies only on ctrl-c 
while 1:
    pass
