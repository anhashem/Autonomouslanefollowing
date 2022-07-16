# EEC195 Camera Initialization Function
#
# Author(s): Abdallah Hashem,Upamanyu Kashyap, Ralph Shehayed, Samuel Miller
#
# This function creates a camera object using the Raspberry Pi's internal camera library.
# It also defines a resolution and framerate at which the camera will capture videos & pictures.
#

import picamera # adding necessary libraries
from picamera.array import PiRGBArray
import time

def CamIni():
    camera = picamera.PiCamera() # define camera object
    camera.resolution = (864,480) # set resolution
    camera.framerate = 120 # set framerate
    rawCapture = PiRGBArray(camera, size=(864,480)) # creates numpy object
    time.sleep(0.1)
    
    return camera # returns object to higher level function 