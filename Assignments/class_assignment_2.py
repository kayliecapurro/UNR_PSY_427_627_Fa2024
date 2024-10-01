# Kaylie Capurro
# PSY 627
# Professor Lescroart
# 10/1/24
# Code Assignment 2

# Create a proto-experiment with multiple different blocks within it, in which 
# the type of stimulus shown changes. You have three different options for what kind 
# of stimuli to work with.

# Option 3: Moving Dots (Figure out how to UPDATE moving dots!)

import numpy as np
import matplotlib.pyplot as plt 
import math 
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches 

# parameters
num_dots = 100
screen_width = 500
screen_height = 500
scatter_data_x = np.random.randn(num_dots)
scatter_data_y = scatter_data_x * 2 + np.random.normal(scale=3, size=(num_dots))
fig, ax = plt.subplots()
dots = ax.plot(scatter_data_x, scatter_data_y, 'o', color='blue')


# create update fuction for animation 
def update(frame):
    for dot in dots:
        x = np.random.rand() * 10
        y = np.random.rand() * 10
        dot.set_data(x, y)
    return dots 


# create each condition of dot movement
def translating_dots():
    #ax.scatter(scatter_data_x, scatter_data_y)
    for dots in dots:
        scatter_data_x = np.random.rand() * 10
        scatter_data_y = np.random.rand() * 10 
    plt.show()


def spiral_dots():
    def update(frame):
    """Update the line object for each frame of the animation."""
    # Generate spiral data
    theta = np.linspace(0, 4 * np.pi, 1000)
    r = a + b * theta
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Rotate the spiral
    angle = np.deg2rad(frame)  # Convert degrees to radians
    x_rot = x * np.cos(angle) - y * np.sin(angle)
    y_rot = x * np.sin(angle) + y * np.cos(angle)

    # Update the line data
    line.set_data(x_rot, y_rot)
    return line,


def expanding_dots():
    arr = np.linspace(1, 50, num_dots)

# create animation layout to plug each condition into 
def create_animation(): 
    fig, ax = plt.subplots()
    #im = ax.imshow(image)
    ax.axis('off')
    ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
    plt.show()


#translating_dots(frames),
create_animation(),
