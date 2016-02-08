#!/usr/bin/python

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import threading
import DynamicObject
DynamicObject = DynamicObject.Class

class Class (threading.Thread):
    def __init__(self, name, API):
        threading.Thread.__init__(self)
        self.name = name
        self.ipc = DynamicObject({})
        self.ipc.extend(API)
        
        # make all functions accessible by default
        for key in vars(self.ipc):
            setattr(self, key, getattr(self.ipc, key))

        # overwriting functions for convenience (and security) - abstracting the 'self' out
        def registerOutput (tag, defaults):
            self.ipc.registerOutput(self, tag, defaults)
        self.registerOutput = registerOutput

        def output (tag, value):
            return self.ipc.output(self, tag, value)
        self.output = output

        def message (msg):
            return self.ipc.message(self, msg)
        self.message = message