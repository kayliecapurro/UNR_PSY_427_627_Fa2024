#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:51:27 2024

@author: kcapurro
"""

from psychopy import visual, core, event
import numpy as np 

# SPIRAL MOTION 
# Create a window
win = visual.Window([800, 800], color=(1,1,1))

# parameters
n_dots = 300
dot_speed = 0.005
dot_size = 0.03
dot_color = (-1, -1, -1)
rotation_speed = 0.03
duration = 20

# create array for intial positions
radii = np.random.uniform(low=0, high=0.5, size=n_dots)
angles = np.random.uniform(low=0, high=2*np.pi, size=n_dots)

# create stimulus
dots = visual.ElementArrayStim(win=win, 
                              nElements=n_dots, 
                              elementTex=None,
                              elementMask='circle',
                              xys=np.zeros((n_dots,2)),
                              sizes = dot_size,
                              colors = dot_color
                              )
# create clock
clock = core.Clock()

# loop for stimulus presentation
while clock.getTime() < duration:
    radii += dot_speed * 0.5
    angles += rotation_speed * 0.5
    # covert polar coordinates to cartesian
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    # update positions of dots
    dots.xys = np.column_stack([x,y])
    dots.draw()
    win.flip()
    
    if 'escape' in event.getKeys():
        break
    
#%%
# EXPANDING MOTION

    
#%%
# Close the window
win.close()
core.quit()
