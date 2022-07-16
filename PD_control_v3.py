# EEC195 PID Control v3
#
# Author(s): Abdallah Hashem,Upamanyu Kashyap, Ralph Shehayed, Samuel Miller
#
# This function implements a PID controller. It takes 6 inputs: The three controller
# constants (Kp, Ki, Kd), the current measured angle and two arrays which store past values.
# The rate of change of angle (error) is determined to find the Derivative term, and the sample based integral
# of angles is used to find the Integral term.
#

def Ave_ang_oldD(kp, ki, kd, curr_ang, arr, bigArr):

  if (len(arr) < 3): # For initial state. If no data is present, array will be populated
    arr.append(curr_ang)
    bigArr.append(curr_ang)
    d_term = 0 # Both D & I terms are zero for the initial state
    i_term = 0

  else: # Once array has three elements, we compute rates of change
    arr.append(curr_ang)
    arr.pop(0)
    bigArr.append(curr_ang)
    d_term = (arr[2]+(arr[1]+arr[0])/2)/2
    i_term = 0
    
    if(len(bigArr) == 5): # We let bigarr get to five terms in length, since it's more reliable for integral calculations.
        i_term = (bigArr[4] + bigArr[3]) / 2 + (bigArr[2] + bigArr[3]) / 2 + (bigArr[1] + bigArr[0])/2 + (bigArr[2] + bigArr[1]) / 2
        bigArr.pop(0)
              
  result = (kp * curr_ang + kd * d_term +  ki * i_term) # Summing result using constants

  return result, bigArr, arr # Returns both arrays and result of PID computation