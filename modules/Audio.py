#!/usr/bin/python

import os
import subprocess
import signal
import time
import inspect

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import IPCThread
IPCThread = IPCThread.Class

import DynamicObject
DynamicObject = DynamicObject.Class

# put your vars here
path = str(os.path.realpath(__file__)).split("/")
path.pop() # remove last element i.e. this filename
strpath = ""
for element in path:
    strpath += element + "/"

class Class (IPCThread):

    def __init__(self, name, API):
        IPCThread.__init__(self, name, API)

        self.registerOutput("audio", {"playing": False})

    def run(self):
        currentSound = None
        while 1:
            time.sleep(0.05)
            servo = self.getInputs().servo
            playing = False
            if (servo.working): playing = True
            if (playing):
                if (currentSound and not self.isPlaying(currentSound)): currentSound = None
                if (not currentSound): currentSound = self.play("cheering.mp3")
            else:
                if (self.isPlaying(currentSound)):
                    self.kill(currentSound)
                    currentSound = None
                    
            self.output("audio", {"playing": playing})
            
    def play (self, filename):
        proc = subprocess.Popen("mpg123 -q " + strpath + filename + "", stdout = subprocess.PIPE, shell = True, preexec_fn=os.setsid)
        return proc

    def kill (self, proc):
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

    def isPlaying (self, proc):
        if (not proc):
            return False
        playing = (proc.poll() == None)
        return playing

