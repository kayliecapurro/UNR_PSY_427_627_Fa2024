# Kaylie Capurro
# 10-10-24
# PSY 627
# Participation Code 3
# Professor Lescroart

import psychopy
from psychopy import visual, core, event
import random
import time 
from pathlib import Path 
import os 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.pyplot as mpimg
import re

# Write a script that computes reaction time from the onset of a particular image in a sequence.
# Have images displayed in a random sequence
# Prompt participant to press a button when a particular category is presented 
# Calculate response time from correct image onset to button press
# Print response time and close window 

# parameters
categories = ['HOUSE', 'FACE', 'BODY', 'CAR', 'CORRIDOR', 'INSTRUMENT', 'NUMBER', 'WORD']
        
# define path to fLoc data
fLoc_path = Path("/home/kcapurro/Desktop/UNR_PSY_427_627_Fa2024/fLoc_stimuli")

# create sorted list of all files in the folder 
def numerical_sort_key(filename):
    return[int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', filename)]

def sort_image_names(fLoc_path):
    folder = Path(fLoc_path)
    image_list = [img.name for img in folder.glob('*')] 
    sorted_images = sorted(image_list, key=numerical_sort_key)
    return(sorted_images)

sorted_image_names = sort_image_names(fLoc_path)
print(sorted_image_names)

# choose random images from floc stimuli file 
def select_random_images(fLoc_path, num_images=10):
    # create path to folder
    folder = Path(fLoc_path)
    # list all images in folder
    image_list = [img for img in folder.glob('*')] 
    # select random images
    selected_images = random.sample(image_list, num_images)
    return selected_images

#try:
random_images = select_random_images(fLoc_path)
#    for img in random_images:
#        random_images.draw()
#        #win.flip()
#        core.wait(.3)
#except ValueError as e:
#    print(e)

# functionality to register button press 
#def button_press():
    

# create window
win = visual.Window([500,500])
# choose random category for participant to react to 
random_category = random.choice(categories)
# tell participant which category they should be reacting to
message = visual.TextStim(win, text=f"Please press a button of your choosing when a {random_category} appears on the screen.")
message.autoDraw = True

# present message
win.flip()
core.wait(3)

#try:
# show images 
image_stim = visual.ImageStim(win, random_images)
image_stim.draw()
win.flip()
core.wait(0.3)
#except ValueError as e:
#    print(e)

# Close window
message.text = 'Closing window'
win.flip()
core.wait(0.3)

win.close()
core.quit()