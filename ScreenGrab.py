## screen grab script
import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import PressKey, ReleaseKey, W, S

#########################################################################
#                                                                       #
# credit to sentdex for the tutoral on reading game frames              #
# https://pythonprogramming.net/game-frames-open-cv-python-plays-gta-v/ #
# and also https://www.youtube.com/channel/UCfzlCWGWYyIQ0aLC5w48gBQ     #
#                                                                       #
#########################################################################

angle = 0

# timers that gives you 4 seconds to get into game
for i in  list(range(4))[::-1]:
    print(i+1)
    time.sleep(1)


# region of intrest takes an image and the vertices that have been defined as arguements
def roi(img, vertices):
    # first step is to create an array that is the same shape as the image
    # using zeros to make sure that the array is blank
    mask = np.zeros_like(img)
    # fill the mask with the vertices
    cv2.fillPoly(mask, # numpy array
                 vertices, # vertices
                 255) # colour set to black
    # Calculates the per-element bit-wise conjunction of two arrays or an array and a scalar.
    masked = cv2.bitwise_and(img, 
                             mask)
    # returns the masked region of intrest
    return masked


# function to draw lines over the image
def draw_lines(img, lines):
    # try-except used if there are no lines detected
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, # draws lines on the img
                 (coords[0],coords[1]), # coordinates 
                 (coords[2],coords[3]), # coordinates
                 [255,255,255], # line colour
                 2) # line thickness in pixles
    except:
        pass # if no lines a detected this will stop the script crashing

# function to process the image
def processed_img(image):
    original_image = image
    #colour change from BGR to gray
    processed_img = cv2.cvtColor(original_image, 
                                 cv2.COLOR_BGR2GRAY)

    # median blur helps remove noise from the image that is being processed
    processed_img = cv2.medianBlur(processed_img,
                                   9)
    # edge detection using Canny 
    processed_img = cv2.Canny(processed_img, 
                              threshold1= 50, # these are tweekable
                              threshold2 = 100) # these are tweekable

    # apply a gaussian blur to smooth edges
    processed_img = cv2.GaussianBlur(processed_img,
                                     (3,3), # kernal size, must be an odd number
                                     0)
  
    # defines the vertices for the region of intrest
    vertices = np.array([[10,500],
                         [10,300],
                         [300,200],
                         [500,200],
                         [800,300],
                         [800,500]])
    # passes the processed image and the vertices to the region of intrest
    processed_img = roi(processed_img, 
                        [vertices])

    # hough line returns an array of arrays that contain the lines
    lines = cv2.HoughLinesP(processed_img, 
                            1, # rho
                            np.pi/180, # theta
                            200, # threshold
                            np.array([]), # empty array
                            150, # minimum line lenght
                            10) # max line gap
    draw_lines(processed_img, lines)


    return processed_img

# last_time = time.time()
# while statement that grabs the screen
while(True):

        # define the size of the screen grab, this grabs the screen at a 800x600 resolution
        # screengrab variable has been converted to a numpy array in this step here
        screengrab = np.array(ImageGrab.grab(bbox=(0,40,800,640)))
        new_screen = processed_img(screengrab)

        # this is just to make sure that the screen grab is getting more the 10fps
        # print('Loop took {} seconds'.format(time.time() - last_time))
        # last_time = time.time()
        cv2.imshow('window', new_screen)
        # using cv2 library to show the image capture, colour correction has been applied using cvtColor
        # cv2.imshow('window', cv2.cvtColor(screengrab, cv2.COLOR_BGR2RGB))
        PressKey(W)

        # press q to quit!!
        if cv2.waitKey(25) & 0xFF == ord('q'):
            # closes the window 
            cv2.destroyAllWindows()
            # we breaking out of the while true loop
            break




