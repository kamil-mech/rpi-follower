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

        self.registerOutput("servo", { "working": False })

    def run(self):
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(18,GPIO.OUT)
        # GPIO.setup(16,GPIO.OUT)

        # self.pwmx = GPIO.PWM(18,50)
        # self.pwmy = GPIO.PWM(16,50)

        # self.pwmx.start(5)
        # self.pwmy.start(5)

        self.working = False
 
        self.currentX = 0
        self.currentY = 0
        self.lastCurrentX = self.currentX
        self.lastCurrentY = self.currentY

        self.currentTime = time.time()
        self.lastRequiredX = 0
        self.lastRequiredY = 0

        self.speed = 10 # up to n degrees per second
        self.deltaTimeController = 1.0 / self.speed # max range for deltatime

        while 1:
            self.updateDeltaTime()
            opencv = self.getInputs().test2
            self.requiredX = opencv.x
            self.requiredY = opencv.y
            if (not self.isInputOk()): # hold servo position if input is faulty
                # do not update current x, y
                self.setWorking(False)
            else:
                if (self.lookingAtTarget()): # reached target
                    # do not update current x, y
                    self.setWorking(False)
                else:
                    # update current x, y
                    if (self.currentX != self.requiredX):
                        directionX = self.getXDirection()
                        self.currentX = self.currentX + int(directionX * self.deltaTime * self.speed)
                        self.clampTooFarX(directionX) # set to required position if went too far while following it
                        self.currentX = self.clamp(self.currentX, -90, 90)
                        self.setWorking(True)

                    if (self.currentY != self.requiredY):
                        directionY = self.getYDirection()
                        self.currentY = self.currentY + int(self.getYDirection() * self.deltaTime * self.speed)
                        self.clampTooFarY(directionY) # set to required position if went too far while following it
                        self.currentY = self.clamp(self.currentY, -90, 90)
                        self.setWorking(True)

            # output to servo no matter what
            # most of work is ensuring values are correct beforehand
            self.lookAtDebugger(self.currentX, self.currentY)

        # pwm.stop()    
        # GPIO.cleanup()

    def lookAtDebugger(self, x, y):
        if (x != self.lastCurrentX or y != self.lastCurrentY): self.message("looking at {}, {}".format(x, y))
        self.lastCurrentX = x
        self.lastCurrentY = y

    def lookAt(self, x, y):
        DCx = 1.9+(0.045*(x+90))
        self.pwmx.ChangeDutyCycle(DCx)
        DCy = 1.9+(0.045*(y+90))
        self.pwmy.ChangeDutyCycle(DCy)

    def isInputOk(self):
        isOk = True
        if (not self.isOk(self.requiredX) or not self.isOk(self.requiredY)):
            if (self.lastRequiredX != self.requiredX or self.lastRequiredY != self.requiredY): self.message("invalid x, y: {}, {}".format(self.requiredX, self.requiredY))
            isOk = False
        
        self.lastRequiredX = self.requiredX
        self.lastRequiredY = self.requiredY
        return isOk

    def isOk(self, coord):
        ok = (type(int(coord)) == int and int(-90) <= int(coord) <= int(90))
        return ok

    def setWorking(self, working):
        if (self.working == working): return
        self.working = working
        self.output("servo", {"working": working})

    def updateDeltaTime(self):
        newTime = time.time()
        self.deltaTime = newTime - self.currentTime
        if (self.deltaTime > self.deltaTimeController): self.currentTime = newTime

    def lookingAtTarget(self):
        looking = (self.requiredX == self.currentX and self.requiredY == self.currentY)
        return looking

    # -1 for decreasing or 1 for increasing
    def getXDirection(self):
        diff = 1
        if (self.requiredX < self.currentX): diff = -1
        return diff

    # -1 for decreasing or 1 for increasing
    def getYDirection(self):
        diff = 1
        if (self.requiredY < self.currentY): diff = -1
        return diff

    def clampTooFarX(self, direction):
        if ((direction == 1 and self.currentX > self.requiredX) or (direction == -1 and self.currentX < self.requiredX)): self.currentX = self.requiredX

    def clampTooFarY(self, direction):
        if ((direction == 1 and self.currentY > self.requiredY) or (direction == -1 and self.currentY < self.requiredY)): self.currentY = self.requiredY

    # currently not used
    def getDifferenceInX(self):
        diff = self.requiredX - self.currentX
        return diff

    # currently not used
    def getDifferenceInY(self):
        diff = self.requiredY - self.currentY
        return diff

    def clamp(self, value, min, max):
        if (value < min): value = min
        elif (value > max): value = max
        return value