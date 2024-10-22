# Kaylie Capurro
# 10-17-24
# PSY 627
# Experiment 1 Trial Script
# Professor Lescroart

import os
import random
import json
import re
from pathlib import Path

# define path to fLoc data
fLoc_path = '/home/kcapurro/Desktop/UNR_PSY_427_627_Fa2024_KC/fLoc_stimuli'

# create sorted list of all files in the folder 
def numerical_sort_key(filename):
    return[int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', filename)]

def category_sort_key(filename):
    image_files = [f for f in os.listdir(fLoc_path) if f.endswith(('.png', '.jpg'))]
# sort images into categories based on file names
    adult_images = [f for f in image_files if 'adult' in f.lower()]
    child_images = [f for f in image_files if 'child' in f.lower()]
    corridor_images = [f for f in image_files if 'corridor' in f.lower()]
    house_images = [f for f in image_files if 'house' in f.lower()]
    car_images = [f for f in image_files if 'car' in f.lower()]
    instrument_images = [f for f in image_files if 'instrument' in f.lower()]
    body_images = [f for f in image_files if 'body' in f.lower()]
    limb_images = [f for f in image_files if 'limb' in f.lower()]
    number_images = [f for f in image_files if 'number' in f.lower()]
    word_images = [f for f in image_files if 'word' in f.lower()]
    scrambled_images = [f for f in image_files if 'scrambled' in f.lower()]
    categories = {'Faces': 
                      {'Adults': adult_images,
                       'Children': child_images},
                   'Places': 
                       {'Corridor': corridor_images,
                        'Houses': house_images},
                   'Objects': 
                       {'Car': car_images,
                        'Instrument': instrument_images},
                   'Bodies':
                       {'Body': body_images,
                        'Limb': limb_images},
                   'Text': 
                       {'Number': number_images,
                        'Word': word_images},
                   'Scrambled':
                       {'Scrambled': scrambled_images}}
    return categories


# sort images by name
def sort_image_names(fLoc_path):
    folder = Path(fLoc_path)
    image_list = [img.name for img in folder.glob('*')] 
    sorted_images = sorted(image_list, key=numerical_sort_key)
    categoried_images = category_sort_key(sorted_images)
    return(categoried_images)

sorted_image_names = sort_image_names(fLoc_path)
categories = sorted_image_names


face_images = categories['Faces']['Adults'] + categories['Faces']['Children']
place_images = categories['Places']['Corridor'] + categories['Places']['Houses']
object_images = categories['Objects']['Car'] + categories['Objects']['Instrument']
bodies_images = categories['Bodies']['Body'] + categories['Bodies']['Limb']
text_images = categories['Text']['Number'] + categories['Text']['Word']
scrambled_images = categories['Scrambled']['Scrambled']

random.shuffle(face_images)
random.shuffle(place_images)
random.shuffle(object_images)
random.shuffle(bodies_images)
random.shuffle(text_images)

# load images
stimuli = {}
for category, subcategories in categories.items():
    stimuli[category] = []
    #for subcat in subcategories:
        # folder_path = os.path.join(fLoc_path)
        # image_files = [os.path.join(folder_path, img) for img in os.listdir(folder_path)]
        # stimuli[category].extend(image_files)


# create specific block orders for subcategories
block_order = [
    {'category': 'Faces', 'images': face_images},
    {'category': 'Places', 'images': place_images},
    {'category': 'Bodies', 'images': bodies_images},
    {'category': 'Text', 'images': text_images},
    {'category': 'Objects', 'images': object_images},
    {'category': 'Scrambled', 'images': scrambled_images},
] * 2  # Repeat each block twice
random.shuffle(block_order)
    


# ensure trials are created correctly for each block
trials = []
for block in block_order:
    block_stimuli = block['images'][:24]  # Get the first 24 images for the block
    repeated_image = random.choice(block_stimuli)  # Select one image to repeat
    block_stimuli.append(repeated_image)  # Include the repeated image
    random.shuffle(block_stimuli)  # Shuffle the stimuli for this block
    # Find the positions of the repeated image
    repeat_positions = [i for i, img in enumerate(block_stimuli) if img == repeated_image]
    second_position = repeat_positions[1] if len(repeat_positions) > 1 else None

    trials.append({
        'category': block['category'],
        'images': block_stimuli,
        'repeated_image':repeated_image,
        'repeated_position': second_position
    })



# save trials to a JSON file for use in the main experiment
with open('trial_sequence.json', 'w') as f:
    json.dump(trials, f)
