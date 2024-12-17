# Kaylie Capurro
# FINAL ASSIGNMENT
# PSY 627
# Professor Lescroart
# 12-17-24


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib

# using this 'TkAgg' because for me on VSCode the animations won't play in the interactive viewer, so this allows them to play automatically. 
# not sure how it will translate to whatever IDE you're using, i imagine it'll work fine, but feel free to comment out if it's a nusiance  
matplotlib.use('TkAgg') 



### MULTIPLE GAUSSIAN CURVES ###
### LEVEL 1 ###
# parameters
n_bells = 50
resolution = 300
colors = plt.cm.cubehelix(np.linspace(0, 1, n_bells))
x = np.linspace(-3, 3, resolution)
amplitudes = np.linspace(0.1, 20, n_bells)
mu = 0
sigmas = np.linspace(0.1, 2, n_bells)

for k in range(n_bells):
    sigma = sigmas[k]
    amplitude = amplitudes[k]
    color = colors[k]
    y = amplitude * np.e ** -(((1/2) * x - mu) / (sigma)) ** 2
    plt.plot(x,y, '-', color=color)



### NOISY SINE WAVE ###
### LEVEL 2 ###
# parameters
x = np.linspace(0, 2 * np.pi, 1000)  
amplitude = 1                       
frequency = 1                       
noise_level = 0.2                   
speed = 0.1                         

# initialize the figure and axis
fig, ax = plt.subplots()
line, = ax.plot(x, np.sin(x), lw=2, label="Noisy Sine Wave")
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)
ax.legend()

# update function for the animation
def update(frame):
    phase = speed * frame  # create a phase shift
    sine_wave = amplitude * np.sin(frequency * x + phase)
    noise = noise_level * np.random.normal(size=x.size)
    line.set_ydata(sine_wave + noise)  # Update line data
    return line,

# create animation
ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)

# show the animation
plt.show()



### MOVING DOT ANIMATION ###
### LEVEL 2 ###
# parameters
x = np.linspace(-5, 5, 1000)             
gaussian = np.exp(-x**2)                    
trajectory_length = len(x)                 
slowdown_factor = 2                    

# speed function, slow at start and end
def speed_profile(t, total_steps):
    normalized_t = t / total_steps          # normalize time (0 to 1)
    return 3 * (normalized_t * (1 - normalized_t))**slowdown_factor

# cumulative sum of speed profile to create trajectory spacing
timesteps = np.arange(trajectory_length)
speeds = speed_profile(timesteps, trajectory_length)
cumulative = np.cumsum(speeds)
cumulative = cumulative / cumulative[-1]   # normalize to fit the entire trajectory

# interpolation to align dot position with animation frames
dot_x = np.interp(np.linspace(0, 1, 200), cumulative, x)
dot_y = np.exp(-dot_x**2)

# initialize the figure and axis
fig, ax = plt.subplots()
ax.plot(x, gaussian, label="Gaussian Line")  
dot, = ax.plot([], [], 'ro', label="Moving Dot")  
ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-0.1, 1.1)
ax.legend()

# update function animation
def update(frame):
    dot.set_data(dot_x[frame], dot_y[frame]) 
    return dot,

# create animation
ani = FuncAnimation(fig, update, frames=len(dot_x), interval=50, blit=True)

# show animation
plt.show()



### SINGLE GAUSSIAN BLOB ###
### LEVEL 2 ###
# parameters
grid_size = 100  
duration = 200   
sigma = 10       
pulse_duration = 100  
slow_factor = 3  

# generate a grid for the gaussian
x = np.linspace(-grid_size // 2, grid_size // 2, grid_size)
y = np.linspace(-grid_size // 2, grid_size // 2, grid_size)
X, Y = np.meshgrid(x, y)

# modulation function for time-varying Gaussian size
def pulse_sigma(t, pulse_duration, base_sigma, slow_factor):
    normalized_t = (t % pulse_duration) / pulse_duration  # normalize to [0, 1]
    phase = np.sin(2 * np.pi * normalized_t)  # cyclic sine wave for in/out motion
    sigmoid_phase = 1 / (1 + np.exp(-slow_factor * (phase - 0.5)))  
    return base_sigma * (1 + 0.5 * sigmoid_phase)  # adjust gaussian spread

# initialize the figure and axis
fig, ax = plt.subplots()
ax.axis("off") 
im = ax.imshow(np.zeros((grid_size, grid_size)), cmap="hot", vmin=0, vmax=1)

# update function for animation
def update(frame):
    current_sigma = pulse_sigma(frame, pulse_duration, sigma, slow_factor)
    gaussian = np.exp(-(X**2 + Y**2) / (2 * current_sigma**2))  
    im.set_array(gaussian)
    return im,

# create animation
ani = FuncAnimation(fig, update, frames=duration, interval=50, blit=True)

# show animation
plt.show()



### AGGREGATION OF GAUSSIAN BLOBS ###
### LEVEL 3 - GRADUATE ASSIGNMENT ###
# parameters
num_blobs = 12  
grid_size = 100  
duration = 200  
sigma = 5  
pulse_duration = 100  
slow_factor = 2  

# generate random blob positions
blob_positions = np.random.randint(-grid_size // 2, grid_size // 2, size=(num_blobs, 2))

# create the grid
x = np.linspace(-grid_size // 2, grid_size // 2, grid_size)
y = np.linspace(-grid_size // 2, grid_size // 2, grid_size)
X, Y = np.meshgrid(x, y)

# function for time-varying Gaussian size
def pulse_sigma(t, pulse_duration, base_sigma, slow_factor):
    normalized_t = (t % pulse_duration) / pulse_duration  # normalize to [0, 1]
    phase = np.sin(2 * np.pi * normalized_t)  # cyclic sine wave
    sigmoid_phase = 1 / (1 + np.exp(-slow_factor * (phase - 0.5)))  
    return base_sigma * (1 + 0.5 * sigmoid_phase)  # adjust gaussian spread

# initialize the plot
fig, ax = plt.subplots()
ax.axis("off")
im = ax.imshow(np.zeros((grid_size, grid_size)), cmap="cubehelix", vmin=0, vmax=1)

# update function for animation
def update(frame):
    grid = np.zeros((grid_size, grid_size))
    
    # add blobs up to the current frame
    for i in range(min(frame // 13 + 1, num_blobs)):  # add a new blob every 10 frames
        blob_x, blob_y = blob_positions[i]
        shifted_X = X - blob_x
        shifted_Y = Y - blob_y
        current_sigma = pulse_sigma(frame, pulse_duration, sigma, slow_factor)
        gaussian = np.exp(-(shifted_X**2 + shifted_Y**2) / (2 * current_sigma**2))
        grid += gaussian  # add the blob to the grid
    
    im.set_array(grid)
    return im,

# create animation
ani = FuncAnimation(fig, update, frames=duration, interval=50, blit=True)

# show aniamtion
plt.show()

