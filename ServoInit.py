# EEC195 Servo Initialization Function
#
# Author(s): Abdallah Hashem,Upamanyu Kashyap, Ralph Shehayed, Samuel Miller
#
# This function creates an object for the I2C servo controller board.
# Within the created object "kit," there exists a servo and a continuous servo.
# The continuous servo object controls the brushless DC motor with pulse widths ranging
# from 1ms to 2ms. The control is done by using the method .throttle, which 
# takes a value from -1 to 1, and translates this into a PWM pulse width
#

# Library imports

from adafruit_servokit import ServoKit 
import board
import busio
import time

def ServoInit():
    i2c = busio.I2C(board.SCL, board.SDA) # Define I2C board pins (SCL & SDA)
    kit = ServoKit(address = 0x40, channels = 16, frequency = 100) # Define address of I2C board & PWM frequency

    kit.continuous_servo[3].set_pulse_width_range(1020,2032) # After oscilloscope measurement and tuning, found that 
    # actual pulse width range (for function) is 1020us to 2032us, which is because the I2C board has some imprecision
    
    kit.continuous_servo[3].throttle = 0 # Initializing throttle to neutral (1.5ms pulse width)
    
    kit.servo[0].set_pulse_width_range(1020,2032) # Same idea with oscilloscope from above
    kit.servo[0].actuation_range = 180 # Defines an actuation range, this is supposed to be the range 
    # of motion for our wheels, but in this application, this figure is arbitrary. 180 degrees denotes full left,
    # 0 degrees denotes right, and 90 denotes straight.
    kit.servo[0].angle = 90 # Initializing the wheels to point straight
    
    time.sleep(2) # Adding 2 second delay, so that the Traxxas ESC has adequate time to see neutral.
    
    return kit