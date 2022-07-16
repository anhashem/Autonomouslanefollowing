# EEC195 CarCont Function
#
# Author(s): Abdallah Hashem,Upamanyu Kashyap, Ralph Shehayed, Samuel Miller
#
# This function contains all code for car to self-drive. Algorithm functions by detecting line
# segments after an image transformation (done with a Hough Transform). After lines are detected,
# angles to normal (horizontal line on plane of camera frame) are computed, and summed up. This perceived
# angle is inputted into a PID controller. This computes a different angle, adjusted for current
# error (perceived angle), rate of change in error and time integral of error. This new angle is 
# sent to a function, Steering.py, which translates this angle into a pulse width which can be 
# used to control the car's speed and throttle. 
#

# Library imports
import picamera
from picamera.array import PiRGBArray
import cv2
import numpy as np
import math
import csv
import time
from adafruit_servokit import ServoKit
import board
import busio
from CamInit import *
from ServoInit import *
from LineThresh import *
from SteeringInit import *
from Steering import *
from PD_control_v3 import *
from PD_control import *
from dataLogger import *



def Carcont(switch):
    
    # Initializing camera, servo
    camera = CamIni()
    kit = ServoInit()

    x = 0 # Used as iterator later on
    arr = [] # Used for collecting recent samples in PID control
    bigarr = [] # Used for collecting recent samples in PID control
    i = 0 # Iterator used later

    # Defining constants for tuning
    # Following three are inputs to Hough Line Transform
    max_slider = 10 
    minLineLength = 10
    maxLineGap = 2

    hardSteerThresh = 10 # Threshold which determines beyond which perceived angle the car will turn fully in either direction  
    straightThresh = 5.4 # Threshold of perceived angle below which car will not make a steering correction
    maxSpeed = 0.3 # Maximum speed of car. Number is a fraction which will be converted into pulse width 
    minSpeed = 0.25 # Minimum speed of car. Converted to pulse width as above

    kp = 0.65 # PID Controller: Kp
    ki = 0 # PID Controller: Ki
    kd = 0.35 # PID Controller: Kd

    # Creation of linear map for steering. y = mx + b calculated given two angle thresholds and speeds.
    # x axis is perceived angle, y axis is steering angle/speed
    slopeFunc, bRight, bLeft, bSpeed, speedGrad = SteeringInit(hardSteerThresh,straightThresh,maxSpeed,minSpeed)

    theta = 0 # Initializing rolling sum for Hough Transform

    # Try/Except logic will interrupt execution if KeyboardInterrupt (ctrl-c) provided in terminal input
    try:

        if(switch is not 0): # From outisde the function. If switch = 1, code will begin
         
            rawCapture = PiRGBArray(camera, size=(864,480)) # Camera capture object as numpy array
            time.sleep(0.01)
            
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True): # Analyzes each captured frame
                
                image = frame.array # Convert captured frame into array 
                edged = LineThresh(image) # function outputs an image that is contoured (refer to LineThresh documentation)
                lines = cv2.HoughLinesP(edged, rho = 1, theta = np.pi/180, threshold = max_slider,minLineLength = minLineLength, maxLineGap = maxLineGap) # Outputs list of line segments given thresholds

                if (lines is not None): # Branch executes if lines are detected in image.                    
                    
                    for x in range (len(lines)-10): # Reduce number of line segments to speed up execution (don't need complete data set to make accurate decisions)
                            
                        for x1, y1, x2, y2 in lines[x]: # (x1,y1) & (x2,y2) are the points that define each line in the frame.
                            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3) # Use of cv2 lines method in order to use it for next calculation
                            theta = theta + np.arctan2((y2 - y1), (x2 - x1)) # Calculating angle to normal (horizontal of camera frame) using arctangent.                 
                    
                    steerAng, bigarr, arr = Ave_ang_oldD(kp,ki,kd,theta,arr,bigarr) # PID controller. Takes perceived angle along with older data to make decision.             

                    # Now compute how fast to run and how hard to steer. Refer to Steering() doucmentation.       
                    ang, throt, decision = Steering(arr,hardSteerThresh, straightThresh, maxSpeed, minSpeed, steerAng, slopeFunc, bSpeed, bLeft, bRight, speedGrad, kit)
                    
                    kit.servo[0].angle = ang # Command car to turn based on computed angle from above
                    kit.continuous_servo[3].throttle = throt # Command car throttle level based on computed speed from above.
                    theta = 0 # Reset rolling sum

                    # Following code is items we used for testing. The series of cv2.imshow() commands display processed images.
                    # Then enters while loop which stops car and awaits key press using WaitKey(). Once key is pressed, car runs briefly,
                    # then stops again and displays new frame.
                     
                    '''
                    #cv2.imshow("Grayscale", gray)
                    #cv2.imshow("blurred", blurred)
                    #cv2.imshow("edged", edged)
                    #cv2.imshow("line detection", image)
                    
                    while(True):
                        kit.continuous_servo[3].throttle = 0

                        if(cv2.waitKey(0)):
                            time.sleep(0.2)
                            #cv2.destroyAllWindows()
                            break
                    '''
                    
                    # Code below performs data logging. Used mostly for testing but turned off during running
                    # due to impact on performance. Data points recorded are controller constants, decision and perceived angle.
                    
                    '''
                    kk = [ki]
                    with open('countries.csv', 'w', encoding='UTF8') as f:
                        
                        writer = csv.writer(f)
                        # write the ki
                        writer.writerow(kk)
                        # write the kp
                        #writer.writerow(kp)
                    
                    t_end = time.process_time() - start
                    input_variable = [
                    ['ki',ki],
                    ['kp', kp],
                    ['kd', kd],
                    ['decision',decision],
                    ['time', t_end]
                    ]
                    '''
                    
                else: # If line is not seen, this branch executes.
                    
                    steerAng, bigarr, arr = Ave_ang_oldD(kp,ki,kd,0,arr,bigarr) # PID control, angle inputted as 0 since no line is seen.
                    # Steering angle and throttle computed below
                    ang, throt, decision = Steering(arr,hardSteerThresh, straightThresh, maxSpeed, minSpeed, steerAng, slopeFunc, bSpeed, bLeft, bRight, speedGrad, kit) 
                    kit.servo[0].angle = ang # Command car to turn based on computed angle from above
                    kit.continuous_servo[3].throttle = throt # Command car throttle level based on computed speed from above.                 
                              
                rawCapture.truncate(0) # Remove old data for next iteration
                    
    except KeyboardInterrupt: # Car will stop and revert to PS4 control.
            
        camera.close()
        
        kit.continuous_servo[3].throttle = 0
    
    
    
    return 0

