# Kaylie Capurro
# 10/1/24
# Professor Lescroart
# Participation Code 2

# Python tiing functions
import psychopy
from psychopy import visual, core
import numpy as np 
import os
import matplotlib.pyplot as plt

#%% Get system timestamp
tx = psychopy.clock.getTime()
# Note that this is in WHOLE SECONDS...

#%% Get time with a clock, starting at a time
# Create a clock object
my_clock = psychopy.clock.Clock()
# Get the time! 
t0 = my_clock.getTime()

#%% Wait a specified duration
t1 = my_clock.getTime(); 
core.wait(2); 
t2 = my_clock.getTime()
print(t2-t1)

#%% Wait for a specified interval
wait_seconds = 3
my_clock2 = psychopy.clock.Clock()
t3 = my_clock2.getTime()
my_timer = core.CountdownTimer(wait_seconds)
while my_timer.getTime() > 0:
    # Do something
    pass
t4 = my_clock2.getTime()

#%%
n_repeats = 100
time_array = []
wait_duration = .1
time_list = np.zeros((n_repeats,))

for i in range(n_repeats):
     t1 = my_clock.getTime(); 
     core.wait(wait_duration); 
     t2 = my_clock.getTime()
     final_t = t1 - t2 
     time_array.append(final_t)
     print(t2-t1)
    
 
st_dev = np.std(time_array)
average = sum(time_array) / len(time_array)
print('standard deviation:', st_dev)
print('average:', -average)

#%%
# Create a small screen window, 
screen_size = [400,400]
win = visual.Window(size=screen_size, 
                    color=(0.5,0.5,0.5),
                    fullscr=False, 
                    units='pix')
win.close()
core.quit()

message = visual.TextStim(win, text='hello world!')
# Drawtrext
message.draw()
flip_time = win.flip()
core.wait(1.0)

#flip_time1 = Screen('Flip', w);
#WaitSecs(.002)
#flip_time2 = Screen('Flip', w);

#print(flip_time2 - flip_time1)



