#!/usr/bin/python
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import time

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import IPCThread
IPCThread = IPCThread.Class

import DynamicObject
DynamicObject = DynamicObject.Class


# Import the face detection haar file
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Used in Screen resolution and positioning later
widths = 340
heights = 180

# initialise servo values
servox = 0
servoy = 0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (widths, heights)
camera.framerate = 32
camera.hflip = True
rawCapture = PiRGBArray(camera, size=(widths, heights))

# allow the camera to warmup
time.sleep(0.1)



# Init the camera and the window
'''cam = cv2.VideoCapture(0)'''
cv2.namedWindow('VideoOutput')






class Class (IPCThread):

    def __init__(self, name, API):
        IPCThread.__init__(self, name, API)

        self.registerOutput("opencv", {"x": 0, "y": 0})

    def run(self):
        while 1:
            self.FaceD()
            break
            cv2.destroyAllWindows()



    ## Function Defonition
    def FaceD(self):

        # Init flags with their default values
        showVideo = True
        textOutput = False
        showAr = True
        showLine = False
        zoomFace = False
        testing = False
        
        # capture frames from the camera
        for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # This is used to store the index of the largest face found
                # This is considered in later code to be the face of interest
                largestFaceIdx = -1
                
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                frame = image.array
                
                # This block grabs an image from the camera and prepares
                # a grey version to be used in the face detection.
                '''(ret,frame) = cam.read()'''
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Run the face detection, and then check if any faces were found
                # faceFound is used later to skip certain section if there is no
                # face found in the input
                faces = face_cascade.detectMultiScale(gray, 2, 5)
                if (len(faces) > 0):
                    faceFound = True
                else:
                    faceFound = False

                if (faceFound) :
                    for idx,(x,y,w,h) in enumerate(faces):
                        largestAreaf = 0
                        if (w*h > largestAreaf):
                            largestAreaf = w*h
                            largestFaceIdxf = idx
                            

                # Output text to stdout
                if(textOutput and faceFound):
                    largest = 0
                    largestArea = 0
                    for idx,(x,y,w,h) in enumerate(faces):
                        if (w*h > largestArea):
                            largestArea = w*h
                            largestFaceIdx = idx
                    print "pos : %r %r" % (largest,faces[largestFaceIdx])

                # Add boxes and lines as an overlay
                if (showAr  and faceFound):
                    for idx,(x,y,w,h) in enumerate(faces):
                        # Used in accurate calculations
                        Face_Wcords = float(w)
                        Face_Hcords = float(h)
                        Face_Xcords = int(float(x + (Face_Wcords/2)))
                        Face_Ycords = int(float(y + (Face_Hcords/2)))
                        Screen_width = float(widths)
                        Screen_height = float(heights)
                        # Magnitude of the text size
                        mag = 0.3
                        # Z co-ords calculated as area screen
                        # divided by area of box around face 
                        maxa = Screen_width * Screen_height
                        maxb = Face_Wcords * Face_Hcords
                        Face_Zcords = float(maxa/maxb)
                                            
                        # Drawing fram around face and center point
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                        cv2.circle(frame, (Face_Xcords, Face_Ycords),2,(0,255,0),2)
                        # Displaying X, Y, Z and Face Index values
                        cv2.putText(frame,"X-Co-Ords=(%r)" % Face_Xcords, (1,20), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,255,0), 2)
                        cv2.putText(frame,"Y-Co-Ords=(%r)" % Face_Ycords, (widths/3,20), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,255,0), 2)
                        cv2.putText(frame,"Z-Co-Ords=(%r)" % Face_Zcords, (2*widths/3,20), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,255,0), 2)
                        cv2.putText(frame,"[%r]" % idx, (x , y - 5), cv2.FONT_HERSHEY_SIMPLEX, .3, (255,0,0), 2)

                        # Calculating servo positions
                        servox = (int((Face_Xcords / Screen_width) *float(180)) -90)
                        servoy = (int((Face_Ycords / Screen_height) *float(180)) -90)
                        self.output("opencv",{"x":servox,"y":servoy})
                        
                        # Displaying servo values
                        cv2.putText(frame,"servoX-Cords=(%r)" % servox, (1,40), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,0,255), 2)
                        cv2.putText(frame,"servoX-Cords=(%r)" % servoy, (widths/3,40), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,0,255), 2)

                        if (testing):
                            # Prints up values to terminal
                            print "%d %d %r" % (Face_Xcords, Face_Ycords, Face_Zcords)
                            # Printing to the terminal
                            print "servo X = %r : servo Y= %r " % (servox, servoy)
                        
                        # Displays line from centre of the screen to 
                        # the centre of the frame around the face
                        if (showLine):
                            cv2.line(frame,(widths/2,heights/2),(x + w/2, y + h/2),(0,0,255),2)

                # Zoom in on the primary face
                if (zoomFace and faceFound):
                    (x,y,w,h) = faces[largestFaceIdx]
                    zoom = frame[y:y+h, x:x+w]
                    frame = cv2.resize(zoom,(widths,heights))

                # Output the video
                if (showVideo):
                    cv2.imshow('VideoOutput', frame)

                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)

                # Check for keypresses
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    print "Q Pressed"
                    break
                if key == ord("v"):
                    print "V Pressed"
                    showVideo = not showVideo
                if key == ord("t"):
                    print "T Pressed"
                    textOutput = not textOutput
                if key == ord("b"):
                    print "B Pressed"
                    showAr = not showAr
                if key == ord("l"):
                    print "L Pressed"
                    showLine = not showLine
                if key == ord("z"):
                    print "Z Pressed"
                    zoomFace = not zoomFace
                if key == ord("e"):
                    print "E Pressed"
                    testing = not testing

        print "Quitting..."
        '''cam.release()'''
        



