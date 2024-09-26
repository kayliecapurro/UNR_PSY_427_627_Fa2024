# Kaylie Capurro
# PSY 627
# Assignment 1
# Professor Lescroart
# 7/16/24

#from unittest.util import sorted_list_difference
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.pyplot as mpimg
from pathlib import Path 
import re
import random
import os
from PIL import Image

# 1 - CREATE A SORTED LIST OF ALL IMAGES IN THE FOLDER
# define path to fLoc data
fLoc_path = Path("/home/kcapurro/Desktop/UNR_PSY_427_627_Fa2024/fLoc_stimuli")
def numerical_sort_key(filename):
    return[int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', filename)]

def sort_image_names(fLoc_path):
    folder = Path(fLoc_path)
    image_list = [img.name for img in folder.glob('*')] 
    sorted_images = sorted(image_list, key=numerical_sort_key)
    return(sorted_images)

sorted_image_names = sort_image_names(fLoc_path)
print(sorted_image_names)


# 2 - SELECT A RANDOM SAMPLE OF 12 IMAGES
def select_random_images(fLoc_path, num_images=12):
    # create path to folder
    folder = Path(fLoc_path)
    # list all images in folder
    image_list = [img for img in folder.glob('*')] 
    # select random images
    selected_images = random.sample(image_list, num_images)
    return selected_images

try:
    random_images  = select_random_images(fLoc_path)
    for img in random_images:
        print(img)
except ValueError as e:
    print(e)


# 3 - DISPLAY EACH OF THE RANDOMLY CHOSEN IMAGES INTO A FIGURE
# create figure
fig, axes = plt.subplots(1, 12, figsize=(15,6))

# plot each image
for i, ax in enumerate(axes.flat):
    img = mpimg.imread(random_images[i])
    ax.imshow(img)
    ax.set_title(f"Image {i+1}")
    ax.axis("off")

plt.tight_layout()
plt.show()


# 4 - CONCATENATE THE IMAGES INTO AN ARRAY AND SAVE
big_image_array = np.array(random_images)
length = big_image_array.size
print(length)
np.save('randomly_selected_images', big_image_array)
print("Images concatenated and saved as randomly_selected_images.npy file.")

# 5 - FOR GRADUATE STUDENTS, MAKE A FIGURE WITH SUBPLOTS TO DISPLAY EACH OF 12 IMAGES IN 4 X 3 LIGHT TABLE GRID
fig, axes = plt.subplots(3, 4, figsize=(15,6))

# plot each image
for i, ax in enumerate(axes.flat):
    img = mpimg.imread(random_images[i])
    ax.imshow(img)
    ax.set_title(f"Image {i+1}")
    ax.axis("off")

plt.tight_layout()
plt.show()