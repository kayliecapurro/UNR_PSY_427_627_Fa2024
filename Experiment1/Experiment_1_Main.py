# Kaylie Capurro
# 10-17-24
# PSY 627
# Experiment 1 Main Script
# Professor Lescroart

from psychopy import visual, core, event, gui
import json
import os
import time
import random

# run trial_script.py first to establish the JSON file needed to call the trial sequence in the main experiment.
# ensure the trial_sequence JSON file lives witin the same directory as main_script.py and trial_script.py. 

# set up participant information
exp_info = {'Participant': '', 'Session': '001'}
dlg = gui.DlgFromDict(dictionary=exp_info, title='Recognition Task')
if dlg.OK == False:
    core.quit()

# load trial sequence
with open('trial_sequence.json', 'r') as f:
    # trials = json.load(f)
    blocks = json.load(f)

# create a data file for saving responses and timing data
filename = f"/home/kcapurro/Desktop/data/{exp_info['Participant']}_session{exp_info['Session']}.txt"
timing_filename = f"/home/kcapurro/Desktop/data/{exp_info['Participant']}_session{exp_info['Session']}_timing.txt"
data_file = open(filename, 'w')
timing_log_file = open(timing_filename, 'w')
data_file.write('block, category, stimulus, response, answer, feedback\n')
timing_log_file.write('block, category, stimulus, onset time, offset time, presentation time, response time\n')

#%%
# create window
win = visual.Window(size=(700,700), fullscr=True, color=(0.5, 0.5, 0.5), units='pix')
fixation = visual.Circle(win, radius=7.5, fillColor='yellow', lineColor='yellow')

# participant instructions
instructions_text = """
In this experiment, you will see images of faces, places, bodies, objects, text, and scrambled images.
You can end the experiment at any time with the 'Esc' key. 
Press a key of your choosing as fast as you can if you see a repeated image.
Press any key to begin.
"""
instructions = visual.TextStim(win, text=instructions_text, color='white', wrapWidth=800, height=30)
instructions.draw()
win.flip()
event.waitKeys()  # wait for any key to continue


def choose_keys():
    button_choice = None
    confirm_choice = None

    while not button_choice:
        select_prompt = visual.TextStim(win, text=("Please select which key you will be using when a repeated image appears on the screen."), wrapWidth=800, height=30)
        select_prompt.draw()
        win.flip()

        keys = event.waitKeys()  # Wait for a key press
        
        # Check if any keys were pressed
        if keys:
            button_choice = keys[0]
            print(f"Participant chose key: {button_choice}")
            confirm = visual.TextStim(win, text=(f"Press '{button_choice}' again to confirm your choice."), wrapWidth=800, height=30)
            confirm.draw()
            win.flip()

            keys = event.waitKeys()  # Wait for confirmation

            # Check if any keys were pressed again
            if keys:
                confirm_choice = keys[0]
                if confirm_choice == button_choice:
                    print('Choice is the same. Moving on.')
                    return confirm_choice
                else:
                    try_again = visual.TextStim(win, text=("First and second keypress do not match. Please try again."))
                    try_again.draw()
                    win.flip()
                    core.wait(3)  # Wait before trying again
                    button_choice = None
                    confirm_choice = None
                    choose_keys()
            else:
                # If no confirmation key is pressed, clear the screen and ask again
                print("No confirmation key pressed, please try again.")
                button_choice = None  # Reset to prompt for key
        else:
            # If no key is pressed, clear the screen and ask again
            print("No key pressed, please try again.")
            button_choice = None  # Reset to prompt for key again


# main experiment loop
#chosen_button = choose_keys()
#response_key = chosen_button  #'space'  
response_key = choose_keys()
trial_clock = core.Clock()
experiment_clock = core.Clock()

# for trial_num, trial in enumerate(trials):
#category = block['category']
block_start = experiment_clock.getTime()



for block_num, block in enumerate(blocks):
    category = block['category']    # E.g., "Faces"
    #subcategories = block['subcategories']  # E.g., ["Adults", "Children"]
    images = block['images']   # All images in this block
    repeated_image = block.get('repeated_image', None)
    repeated_image_position = block.get('second_position', None)

    # shuffle images within the block (random mix of subcategories)
    #random.shuffle(category)
    
    # run block of trials
    for img_path in images:
        # draw fixation dot
        fixation.draw()
        win.flip()
        
        # check for 'escape' key press to exit the experiment early
        if event.getKeys(keyList=['escape']):
            break
            # close the window
            win.close()
            core.quit()
            
        im_path = f'/home/kcapurro/Desktop/UNR_PSY_427_627_Fa2024_KC/fLoc_stimuli/{img_path}'    
        
        # draw and present image
        img = visual.ImageStim(win, image=im_path, size=(500, 500))
        img.draw()
        fixation.draw()  
        win.flip()

        onset_time = trial_clock.getTime()
        response = None
        response_time = None
        feedback = 'none'
        answer = False
        key_pressed = None
        subcategory = 'Adult' if 'adult' in img_path.lower() else 'Child' if 'child' in img_path.lower() else 'Other'


        
        keys = event.waitKeys(maxWait=0.5, keyList=[response_key, 'escape'], timeStamped=trial_clock)
        if keys:
            key_pressed, response_time = keys[0]
            
            # check for escape key during image presentation
            if key_pressed == 'escape':
                print("Escape key pressed. Shutting down experiment")
                data_file.close()
                timing_log_file.close()
                win.close()
                core.quit()

            # check if the image was a repeat
            if img_path == repeated_image:
                answer = True
                feedback = 'green'
            else:
                answer = False
                feedback = 'red'


            # provide feedback by changing fixation dot color
            fixation.fillColor = feedback
            fixation.lineColor = feedback
            fixation.draw()
            win.flip()
            core.wait(2)  
            fixation.fillColor = 'yellow'  
            fixation.lineColor = 'yellow'

        offset_time = trial_clock.getTime()
        presentation_time = onset_time - offset_time 

        # write data to file
        timing_log_file.write(f"{block_num},{category},{subcategory},{os.path.basename(img_path)},{onset_time},{offset_time},{presentation_time:.3f}, {response_time}\n")
        data_file.write(f"{block_num},{category},{subcategory},{os.path.basename(img_path)},{key_pressed},{response_time},{onset_time},{answer},{feedback}\n")


        # wait for gap duration (0.1 seconds)
        win.flip()
        
        core.wait(0.1)

    # ensure block is exactly 12 seconds long
block_duration = experiment_clock.getTime() - block_start
if block_duration < 12:
    core.wait(12 - block_duration)

# end screen
end_text = "You have finished the experiment. Thank you!"
end_screen = visual.TextStim(win, text=end_text, color='white', height=30)
end_screen.draw()
win.flip()
event.waitKeys()  # wait for a key press to finish

# close the data file and window
timing_log_file.close()
data_file.close()
win.close()
core.quit()
