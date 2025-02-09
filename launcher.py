#!/usr/bin/env python3
import signal
import RPi.GPIO as GPIO
import threading
import time
import argparse
import os
import random
import subprocess

##########################################
calendar_url1 = "https://ics.calendarlabs.com/75/e62b6480/UK_Holidays.ics"
calendar_url2 = "https://ics.calendarlabs.com/75/e62b6480/UK_Holidays.ics"
##########################################

# Argument parsing setup
parser = argparse.ArgumentParser(description='Button-based launcher with timed functionality.')
parser.add_argument('--photo-input-dir', type=str, required=True,
                    help='Directory for photo input')
parser.add_argument('--delay', type=int, default=300,
                    help='Delay time in seconds for the base function loop')
args = parser.parse_args()

# Ensure the input directory has a trailing slash (not strictly required if we use os.path.join, but often convenient).
# You can skip this if you always use os.path.join(photo_input_dir, random_image).
if not args.photo_input_dir.endswith(os.sep):
    args.photo_input_dir += os.sep

history_file = '/home/pi/eink_tools/shown_image_history.txt'

# A threading lock to ensure no race conditions between the timed loop and button callbacks
pick_image_lock = threading.Lock()

def pick_random_image(photo_input_dir, history_file):
    with pick_image_lock:
        # Read the history of selected images (filenames only)
        if os.path.exists(history_file):
            with open(history_file, 'r') as file:
                selected_images = file.read().splitlines()
        else:
            selected_images = []

        # Acceptable image extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

        # Gather all image filenames in the directory
        all_images = [
            fname for fname in os.listdir(photo_input_dir)
            if any(fname.lower().endswith(ext) for ext in image_extensions)
        ]

        # Safety check: if there are no images, return None or handle error
        if not all_images:
            print("No images found in directory:", photo_input_dir)
            return None

        # Filter out images that have already been selected
        unselected_images = [img for img in all_images if img not in selected_images]

        if unselected_images:
            # Pick a random unselected image
            random_image = random.choice(unselected_images)
        else:
            # All images have been shown; reset history and pick again
            open(history_file, 'w').close()  # Clear the file
            random_image = random.choice(all_images)

        # Update history by appending this new choice
        with open(history_file, 'a') as file:
            file.write(random_image + '\n')

        # Return the full path to the chosen image
        return os.path.join(photo_input_dir, random_image)


def base_function():
    """Displays a random image on the Inky display."""
    image_path = pick_random_image(args.photo_input_dir, history_file)
    if image_path:
        subprocess.run(['python3', "/home/pi/Pimoroni/inky/examples/7color/image.py", image_path])
    else:
        print("Skipping display update (no image found).")


######################
###BUTTON FUNCTIONS###
######################

def function_a():
    # Execute the bus_countdown script twice (with 60s pause), then return to the photo cycle
    subprocess.run(['python3', "/home/pi/eink_tools/bus_countdown.py"])
    time.sleep(60)
    subprocess.run(['python3', "/home/pi/eink_tools/bus_countdown.py"])
    time.sleep(60)
    base_function()

def function_b():
    # Download ICS files, show day calendar, then return to photo cycle
    subprocess.run(['wget', calendar_url1, "-O", "calendar/js/calendar_input1.ics"])
    subprocess.run(['wget', calendar_url2, "-O", "calendar/js/calendar_input2.ics"])
    subprocess.run(['python3', "/home/pi/eink_tools/day_calendar_launch.py"])
    time.sleep(180)
    base_function()

def function_c():
    # Download ICS files, show month calendar, then return to photo cycle
    subprocess.run(['wget', calendar_url1, "-O", "calendar/js/calendar_input1.ics"])
    subprocess.run(['wget', calendar_url2, "-O", "calendar/js/calendar_input2.ics"])
    subprocess.run(['python3', "/home/pi/eink_tools/month_calendar_launch.py"])
    time.sleep(180)
    base_function()

def function_d():
    print("Function D executed")
    time.sleep(180)
    base_function()

######################
# TIMED LOOP THREAD  #
######################

def timed_loop():
    while True:
        base_function()
        time.sleep(args.delay)

# Start the timed loop in a separate thread
threading.Thread(target=timed_loop, daemon=True).start()

######################
# GPIO SETUP & MAIN  #
######################

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]
LABELS = ['A', 'B', 'C', 'D']
FUNCTIONS = [function_a, function_b, function_c, function_d]

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print(f"Button press detected on pin: {pin}, label: {label}")
    FUNCTIONS[BUTTONS.index(pin)]()  # Execute the corresponding function

for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=handle_button, bouncetime=250)

# Prevent the script from exiting
signal.pause()
