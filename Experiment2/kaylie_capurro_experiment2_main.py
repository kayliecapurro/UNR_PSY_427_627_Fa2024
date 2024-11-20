# Kaylie Capurro
# 11-19-24
# PSY 627
# Experiment 2 Main Script
# Professor Lescroart

import os
import json
from psychopy import visual, core, event, gui
import kaylie_capurro_experiment2_trial

screen_size = (800,600)
fullscreen_binary = False
background_color = "black"
trial_duration_total = 1.6

def get_matching_images(directory, pattern):
    return [os.path.join(directory, f) for f in os.listdir(directory) if pattern in f and f.endswith(('.png', '.jpg'))]

def collect_responses():
    dlg = gui.Dlg(title="Set Response Keys")
    dlg.addField("Key for 'Same':", "z")
    dlg.addField("Key for 'Different':", "m")
    user_input = dlg.show()
    if not dlg.OK:
        core.quit()
    return {"same": user_input[0], "different": user_input[1]}

def setup_screen(size=screen_size, fullscreen=fullscreen_binary, color=background_color):
    return visual.Window(size=size, fullscr=fullscreen, color=color, units="pix")

def main():
    # get participant info
    info = {"Participant ID": ""}
    dlg = gui.DlgFromDict(info)
    if not dlg.OK:
        core.quit()
    participant_id = info["Participant ID"]

    # create presentation window 
    win = setup_screen(size=screen_size, fullscreen=fullscreen_binary, color=background_color)

    # load images
    image_directory = "/home/kcapurro/Desktop/UNR_PSY_427_627_Fa2024_KC/fLoc_stimuli/"
    images = get_matching_images(image_directory, "")  
    print(f"Loaded {len(images)} images from {image_directory}")

    # generate trial JSON file
    json_file = "trial_plan.json"
    if not os.path.exists(json_file):
        kaylie_capurro_experiment2_trial.generate_trial_json(images, json_file)

    with open(json_file, "r") as f:
        trials = json.load(f)

    print(f"Loaded {len(trials)} trials from {json_file}")

    # collect participant response keys
    response_keys = collect_responses()

    # create log file
    log_file_name = f"log_{participant_id}.csv"
    with open(log_file_name, "w") as log_file:
        log_file.write("Trial, Image1, Image2, Response, RT(s), Correct\n")

        instructions = visual.TextStim(
            win,
            text=f"Press '{response_keys['same']}' for image pairs that are the same, "
                 f"and press '{response_keys['different']}' for different.\nIf at anytime you would like to end the experiment, please press the 'escape' key.\nPress any key to start.",
            color="white"
        )
        instructions.draw()
        win.flip()
        event.waitKeys()

        # run trials
        for idx, trial_data in enumerate(trials):
            phase_start = core.getTime()
            response, rt, correct = kaylie_capurro_experiment2_trial.run_trial(win, trial_data, response_keys)
            log_file.write(f"{idx+1},\n{trial_data['images'][0]},\n{trial_data['images'][1]},\n {response},{f'{rt:.4f}' if rt is not None else 'N/A'},{correct}\n")

            wait_msg = visual.TextStim(win, text="Press any key to continue to the next trial", color="white")
            wait_msg.draw()
            win.flip()
            event.waitKeys()

            # inter-trial interval
            while core.getTime() - phase_start < trial_duration_total:  
                pass

    end_message = visual.TextStim(win, text="Thank you for participating!", color="white")
    end_message.draw()
    win.flip()
    core.wait(2)
    win.close()

if __name__ == "__main__":
    main()

