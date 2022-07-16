# EEC195 Top Level Function (main.py)
#
# Author(s): Abdallah Hashem,Upamanyu Kashyap, Ralph Shehayed, Samuel Miller
#
# This function contains the rest of the code execution. A class is created for the PS4 Controller we use.
# Within the class, we define methods that are triggered by button presses on the controller. When this function
# runs, the user has 60 seconds to connect a PS4 controller, after which the car can be driven using the controller.
# When the PlayStation button is pressed, the car begins running in self-driving lane following mode.
# Once in self-driving mode, the execution can be stopped and control returned to the PS4 controller by using a 
# keyboard interrupt (Ctrl-C).
#

# Library imports

from pyPS4Controller.controller import Controller
from CarCont import *
import time
from ServoInit import *

# Initializing servo object, kit (refer to documentation in ServoInit.py)
kit = ServoInit()

# Setting up class for PS4 Controller. Each method is an action taken on the controller.
class MyController(Controller):

    def __init__(self,**kwargs): # Initializing 
        Controller.__init__(self, **kwargs)
    
    def on_x_press(self): # When "x" pressed, car will move forward at pulse width of 1.7ms
        kit.continuous_servo[3].throttle = 0.4
    
    def on_x_release(self): # When "x" released, car will stop (goes into neutral, 1.5ms pulse width )
        kit.continuous_servo[3].throttle = 0
    
    def on_right_arrow_press(self): # When right arrow on D-pad pressed, car will turn fully to right (1ms pulse width)
        kit.servo[0].angle = 0
    
    def on_left_arrow_press(self): # When left arrow on D-pad pressed, car will turn fully to left (2ms pulse width)
        kit.servo[0].angle = 180

    def on_left_right_arrow_release(self): # When left/right D-pad buttons released, wheels will point straight (1.5ms pulse width) 
        kit.servo[0].angle = 90
    
    def on_playstation_button_press(self): # When PlayStation button pressed, car will enter self-driving mode  
        Carcont(1)
        
    def on_down_arrow_press(self): # When down D-pad button pressed, car will reverse with pulse width of 1.3ms 
        kit.continuous_servo[3].throttle = -0.4
    
    def on_up_down_arrow_release(self): # When up/down D-pad buttons released, throttle will reset to neutral (1.5ms pulse width)
        kit.continuous_servo[3].throttle = 0


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False) # Putting above class definition into callable object "controller"

controller.listen(timeout = 60) # Car begins looking for bluetooth connection to controller. If no connection established within 60 seconds of execution, code stops
