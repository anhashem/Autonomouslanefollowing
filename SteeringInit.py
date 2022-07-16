# EEC195 Linear Steering Initialization Function
#
# Author(s): Abdallah Hashem,Upamanyu Kashyap, Ralph Shehayed, Samuel Miller
#
# This function initializes the car's steering algorithm. We use a linear mapping
# to translate angles from either a PID controller or straight from the camera into
# an angle between zero and 180 degrees, which is used to convert into a pulse width
# which the car's servo uses to turn. 
# The function also uses a similar linear mapping to compute speed (Outputs number
# between 0 and 1).
#

def SteeringInit(hardSteerThresh, straightThresh, maxSpeed, minSpeed):
    
    slopeFunc = 90 / (hardSteerThresh - straightThresh) # Computes gradient of linear portion
    bRight = 0 - (-hardSteerThresh * slopeFunc) # Computes y-intercept of right turn line
    bLeft = 90 - (straightThresh * slopeFunc) # Computes y-intercept of left turn line
    
    speedGrad = (minSpeed - maxSpeed) / (hardSteerThresh - straightThresh) # Computes gradient of speed linear control
    bSpeed = maxSpeed - speedGrad * (straightThresh) # Computes y intercept of speed controller

    return slopeFunc, bRight, bLeft, bSpeed, speedGrad # Returns parameters which are used by Steering() (refer to Steering.py for docs)