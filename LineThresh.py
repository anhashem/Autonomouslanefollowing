# EEC195 Image Processing Function
#
# Author(s): Abdallah Hashem,Upamanyu Kashyap, Ralph Shehayed, Samuel Miller
#
# This function takes an image as an input, and performs various image processing algorithms on it.
# First, it converts the image into grayscale, which makes it easier for us to separate a white line
# from a grey background. Then, it blurs the image, which makes it easier to detect edges. 
# Finally, it runs an algorithm called Canny(), which draws contours over the detected edges.
#

# CV2 libary import 
import cv2

def LineThresh(image):

    Binary_visible = True
    
    # Grayscale thresholds
    threshold1 = 20
    threshold2 = 255
    
    # Input params for Gaussian blur
    k_width = 3
    k_height = 3

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (k_width, k_height), 0)
    edged = cv2.Canny(blurred, threshold1, threshold2)

    return edged