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

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
#print " Values must be between -90 and 90"




# put your vars here

class Class (IPCThread):

    def __init__(self, name, API):
        IPCThread.__init__(self, name, API)

        self.registerOutput("servo", { "working": False })

    def run(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(18,GPIO.OUT)
        GPIO.setup(16,GPIO.OUT)

        t = 0.06

        pwmx = GPIO.PWM(18,50)
        pwmy = GPIO.PWM(16,50)

        pwmx.start(5)
        pwmy.start(5)
        working = False
 
        currentx = 0
        currenty = 0
        while 1:
            opencv = self.getInputs().opencv
            x = opencv.x
            y = opencv.y

            
            if type(int(x)) == int and int(-90) <= int(x) <= int(90):
                requiredx = int(x)
                
                while currentx < requiredx:
                    currentx = currentx + 1
                    DCx = 1.9+(0.045*(currentx+90))
                    working = True
                    self.output("servo",{"working": working})
                    #print "%r" % DC
                    pwmx.ChangeDutyCycle(DCx)
                    time.sleep(t)
                    
                        
                while currentx > requiredx:
                    currentx = currentx - 1
                    DCx = 1.9+(0.045*(currentx+90))
                    working = True
                    self.output("servo",{"working": working})  
                    #print "%r" % DC
                    pwmx.ChangeDutyCycle(DCx)
                    time.sleep(t)          

            if type(int(y)) == int and int(-90) <= int(x) <= int(90):
                requiredy = int(y)
            
                while currenty < requiredy:
                    currenty = currenty + 1
                    DCy = 1.9+(0.045*(currenty+90))
                    working = True
                    self.output("servo",{"working": working})
                    #print "%r" % DC
                    pwmy.ChangeDutyCycle(DCy)
                    time.sleep(t)
                        
                while currenty > requiredy:
                    currenty = currenty - 1
                    DCy = 1.9+(0.045*(currenty+90))
                    working = True
                    self.output("servo",{"working": working})
                    #print "%r" % DC
                    pwmy.ChangeDutyCycle(DCy)
                    time.sleep(t)


            
            working = False
            self.output("servo",{"working": working})

        pwm.stop()    
        GPIO.cleanup()

