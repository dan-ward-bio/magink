#!/usr/bin/env python3

import signal
import RPi.GPIO as GPIO
import threading
import time
import argparse
import os
import random
import subprocess

# Argument parsing setup
parser = argparse.ArgumentParser(description='Button-based launcher with timed functionality.')
parser.add_argument('--photo-input-dir', type=str, required=True, help='Directory for photo input')
parser.add_argument('--delay', type=int, default=300, help='Delay time in seconds for the base function loop')
args = parser.parse_args()

######################
####BASE FUNCTIONS####
######################

#Function for selecting a rnadom photo for the base function slideshow
def pick_random_image(photo_input_dir):
    # List of image file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

    # List all files in the directory
    files = os.listdir(photo_input_dir)

    # Filter out files that are images
    image_files = [file for file in files if any(file.lower().endswith(ext) for ext in image_extensions)]

    # Pick a random image file
    if image_files:
        random_image = random.choice(image_files)
        full_image_path = os.path.join(photo_input_dir, random_image)
        return full_image_path
    else:
        return None


# Base function using the photo input directory
def base_function():
    # Execute the other script
    subprocess.run(['python', "/home/pi/Pimoroni/inky/examples/7color/image.py", pick_random_image(args.photo_input_dir)])


######################
###BUTTON FUNCTIONS###
######################



# Functions for each button press
def function_a():
    # Execute the bus_countdown script
    subprocess.run(['python', "bus_countdown.py"])

def function_b():
    print("Function B executed")

def function_c():
    print("Function C executed")

def function_d():
    print("Function D executed")

# Function to handle the timed loop
def timed_loop():
    while True:
        base_function()
        time.sleep(args.delay)  # Use delay time from arguments

# Start the timed loop in a separate thread
threading.Thread(target=timed_loop, daemon=True).start()

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C, and D respectively
LABELS = ['A', 'B', 'C', 'D']
FUNCTIONS = [function_a, function_b, function_c, function_d]

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# "handle_button" will be called every time a button is pressed
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))
    FUNCTIONS[BUTTONS.index(pin)]()  # Execute the corresponding function

# Loop through our buttons and attach the "handle_button" function to each
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=handle_button, bouncetime=250)

# Prevent the script from exiting
signal.pause()
