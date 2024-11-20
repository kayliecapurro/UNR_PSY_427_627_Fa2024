# Kaylie Capurro
# 11-19-24
# PSY 627
# Experiment 2 Trial Script
# Professor Lescroart

import json
import random
from psychopy import visual, core, event

stimulus_size = (500,500)
fixation_symbol = "+"
fixation_color = 'white'
fixation_time = 0.1
image_presentation_time = 0.1
inter_stimulus_inteval = 0.5
num_trials = 30
feedback_duration = 1

def generate_trial_json(images, output_path, n_trials=num_trials):
    trials = []
    for _ in range(n_trials // 2):
        # Same image trial
        img_pair = random.sample(images, 1) * 2 
        trials.append({"images": img_pair, "correct": "same"})

        # Different image trial
        img_pair = random.sample(images, 2)  
        trials.append({"images": img_pair, "correct": "different"})

    random.shuffle(trials)  

    # save to JSON file
    with open(output_path, "w") as f:
        json.dump(trials, f, indent=4)
    print(f"trial plan saved to: {output_path}")

def run_trial(win, trial, response_keys):
    # prepare stimuli
    img1 = visual.ImageStim(win, image=trial["images"][0], size=stimulus_size)
    img2 = visual.ImageStim(win, image=trial["images"][1], size=stimulus_size)
    fixation = visual.TextStim(win, text=fixation_symbol, color=fixation_color)

    # create fixation cross
    fixation.draw()
    win.flip()
    fixation_start = core.getTime()
    while core.getTime() - fixation_start < fixation_time: 
        pass

    # show first image
    img1.draw()
    win.flip()
    img1_start = core.getTime()
    while core.getTime() - img1_start < image_presentation_time:  
        pass
    img1_end = core.getTime()
    print(f"image 1 presentation time: {img1_end - img1_start:.6f} seconds")

    # inter-stimulus interval
    fixation.draw()
    win.flip()
    isi_start = core.getTime()
    while core.getTime() - isi_start < inter_stimulus_inteval:  
        pass

    # show second image
    img2.draw()
    win.flip()
    img2_start = core.getTime()
    while core.getTime() - img2_start < image_presentation_time:  
        pass
    img2_end = core.getTime()
    print(f"image 2 presentation time: {img2_end - img2_start:.6f} seconds")

    # collect participant response
    fixation.draw()
    win.flip()
    response = None
    rt_clock = core.Clock()
    keys = event.waitKeys(maxWait=15, keyList=[response_keys["same"], response_keys["different"], "escape"], timeStamped=rt_clock)

    # escape key implementation
    if keys:
        response, rt = keys[0]
        if response == "escape":
            win.close()
            core.quit()
    else:
        response, rt = None, None

    # provide participant with feedback
    correct = response == response_keys.get(trial["correct"])
    fixation.color = "green" if correct else "red"
    fixation.draw()
    win.flip()
    core.wait(feedback_duration)  

    return response, rt, correct

