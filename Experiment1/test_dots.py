#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:51:27 2024

@author: kcapurro
"""

from psychopy import visual, core, event
import numpy as np 
import math
import random


# TRANSLATE MOTION
# parameters
n_dots = 250
dot_speed = 0.05
dot_size = 8
expansion_limit = 400
base_distance = 300
black = (-1, -1, -1)
white = (1, 1, 1)

# create window
win = visual.Window([800, 800], color=white, units='pix')

# create list of random angles
angles = np.random.uniform(0, 2*np.pi, n_dots)

# set initial postitions for dots
radii = np.random.uniform(base_distance, base_distance + 5, n_dots)
x = radii * np.random.uniform(angles)
y = radii * np.random.uniform(angles)


# create dot stimulus object 
dots = visual.ElementArrayStim(win=win,
                              nElements=n_dots,
                              elementTex=None,
                              elementMask='gauss',
                              sizes=dot_size,
                              xys=np.column_stack([x,y]),
                              colors=black,
                              )



# TRANSLATION FUNCTION
# translation motion parameters
def translate(duration, translation_speed = 1):
    translation_direction = np.array([-1,-1])
    expansion = False
    timer = core.Clock()
    while timer.getTime() < duration:
        xys = dots.xys + translation_speed * translation_direction
        dots.xys = xys
        
        dots.draw()
        win.flip()
    


#SPIRAL FUNCTION
def spiral_motion(duration, spiral_speed=0.02):
    rotation_speed = 0.02
    spin_radii = np.random.uniform(low=0, high=250, size=n_dots)
    spin_angles = np.random.uniform(low=0, high=2*np.pi, size=n_dots)
    timer = core.Clock()
    while timer.getTime() < duration:
        spin_radii += dot_speed * 0.5
        spin_angles += rotation_speed * 1
    # covert polar coordinates to cartesian
        x = spin_radii * np.cos(spin_angles)
        y = spin_radii * np.sin(spin_angles)
    # update positions of dots
        dots.xys = np.column_stack([x,y])
        dots.draw()
        win.flip()



# FUNCTION EXPANDING MOTION

def expanding(duration, expansion_speed=3):
    global radii
    expansion = True
    timer = core.Clock()
# animation 
    while timer.getTime() < duration:
        # Update radius for expansion/contraction
        if expansion:
            radii += expansion_speed
        else:
            radii -= expansion_speed
    
        if radii.max() > expansion_limit:
            expansion = False
        elif radii.min() < base_distance:
            expansion = True
        
        x = radii * np.cos(angles)
        y = radii * np.sin(angles)
        dots.xys = np.column_stack([x, y])

        dots.draw()
        win.flip()

    
    
 # function to run blocks
def run_block(duration, stimulus_function, gap=2):
    stimulus_function(duration)
    core.wait(gap)
    
stimuli = [translate, spiral_motion, expanding]
for stimulus in stimuli:
    run_block(20, stimulus, gap=3)
    
for i in range(2):
    speed_modifier = 1 if i == 0 else 2
    for stimulus in stimuli:
        run_block(2 * speed_modifier, stimulus, gap=0.5)

# Close the window
win.close()
core.quit()
