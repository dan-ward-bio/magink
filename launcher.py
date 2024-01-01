#!/usr/bin/env python3

import signal
import RPi.GPIO as GPIO
import threading
import time

def base_function():
    # Replace this with your own base function logic
    print("Executing base function...")

def function_a():
    print("Function A executed")

def function_b():
    print("Function B executed")

def function_c():
    print("Function C executed")

def function_d():
    print("Function D executed")

# Function to handle the 5-minute loop
def timed_loop():
    while True:
        base_function()
        time.sleep(300)  # Wait for 5 minutes

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
