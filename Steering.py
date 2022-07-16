# EEC195 Steering Function 
#
# Author(s): Abdallah Hashem,Upamanyu Kashyap, Ralph Shehayed, Samuel Miller
#
# This function takes computed linear function parameters and translates them into a number between zero and 180
# (for steering), and between zero and one (for throttle). This is done by using y = mx + b linear equations, 
# where the values for m and b are computed in SteeringInit() (refer to SteeringInit.py for docs)
#

# Only one library import
import math

def Steering(arr,hardSteerThresh, straightThresh, maxSpeed, minSpeed, theta,slopeFunc, bSpeed, bLeft,bRight, speedGrad, kit):

    # Follows piecewise linear mapping. If within a certain x-bound, the code enters a branch
    if(abs(theta) < straightThresh): # If the angle is not high enough, car will drive straight
        angle = 90
        throttle = maxSpeed
        decision = "straight"

    elif (theta < hardSteerThresh and theta > 0): # Linear steering & speed for left turn
        angle = int(bLeft + (theta * slopeFunc))
        throttle = speedGrad * abs(theta) + bSpeed
        decision = "linear left"

    elif(theta > -hardSteerThresh and theta < 0): # Linear steering & speed for right turn
        angle = int(bRight + (theta * slopeFunc))
        throttle = speedGrad * abs(theta) + bSpeed
        decision = "linear right" 

    elif(theta > hardSteerThresh): # Beyond threshold, car will turn all the way left and slow down to minSpeed
        angle = 180
        throttle = minSpeed
        decision = "strong left"

    else: # Beyond threshold, car will turn all the way right and slow down to minSpeed.
        angle = 0
        throttle = minSpeed
        decision = "strong right"
        
    return angle, throttle, decision # Returns results to upper level function. 
    
