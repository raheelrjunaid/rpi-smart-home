# RPI Keypad Function
# Author: Raheel Junaid
# Date Started: 1/23/21

from global_vars import buzzer, screen, armSystem, disarmSystem, showSystemStatus, RGBLed, remote_factory
import os
from dotenv import load_dotenv, set_key
from gpiozero import DigitalOutputDevice
from threading import Thread
from time import sleep
from colorzero import Color
from pad4pi import rpi_gpio
from signal import pause
from time import time

load_dotenv()

# Keypad setup
KEYPAD = [
    [1, 2, 3, 'A'],
    [4, 5, 6, 'B'],
    [7, 8, 9, 'C'],
    ['*', 0, '#', 'D']
]

ROW_PINS = [12, 16, 20, 21]
COL_PINS = [6, 13, 19, 26]

factory = rpi_gpio.KeypadFactory()

KEY = os.getenv('KEY')

keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

# Default Key Mode
keymode = 'enter'
startTime = time()
trycode = ''
triggerCount = 0
cancelRFIDTimer = DigitalOutputDevice(26, pin_factory=remote_factory)

def startTimer():

    global trycode
    global startTime
    while True:

        if int(time() - startTime) > 3:
            showSystemStatus()
            trycode = ''

        sleep(1)

def tryKey(key):

    # Import globals (required as function doesn't allow args)
    global trycode
    global startTime
    global keymode
    global KEY
    
    startTime = time()

    buzzer.beep(0.2, n=1)

    trycode += str(key)
    print(trycode, keymode)

    # Working key attempt function
    def enterKey(key, trycode, keymode):
        screen.text('Attempt', 1)
        global triggerCount

        # Reset Code
        if key == '*':
            if trycode == '*':
                armSystem() # Arm security system on * press
                screen.text('System ARMED', 1)
            else:
                print('reset code') # Unless their in the middle of typing out their code
            trycode = ''

        # Change key mode to begin changing keycode
        elif key == '#':
            trycode = ''
            keymode = 'change'
            newKey(key, trycode, keymode, KEY)

        # Read code attempt and compare to actual KEY
        else:
            if len(trycode) == 4:
                if trycode == KEY:
                    print('success')
                    cancelRFIDTimer.on()
                    RGBLed.color = Color('green')
                    disarmSystem()
                    screen.text('Attempt Passed', 1)
                    screen.text('', 2)
                    buzzer.beep(0.1, 0.1, n=2)
                    triggerCount = 0 
                    sleep(1)
                else:
                    print('failure')
                    RGBLed.color = Color('red')
                    buzzer.beep(0.1, 0.1, n=3)
                    screen.text('Attempt Failed', 1)
                    screen.text('', 2)
                    triggerCount += 1
                trycode = ''

        # return values to change (no global var writing)
        return trycode, keymode

    # Working change keycode function
    def newKey(key, trycode, keymode, KEY):
        screen.text('Change', 1)

        # Beginning prompt
        if len(trycode) == 0:
            print('Input 4 digit code')

        # Read code change and apply change to global KEY (not global)
        elif len(trycode) == 4:

            # Backend set
            set_key('.env', 'KEY', trycode)

            # Apply change in front
            KEY = trycode
            screen.text(f'to {trycode}', 2)
            trycode = ''
            keymode = 'enter'

            # Show new code breifly
            sleep(1)
            screen.text('Attempt', 1)
            buzzer.beep(0.2, 0.1, n=3)

        # return values to change (no global var writing)
        return trycode, keymode, KEY

    # Runtime statement using global keymode
    # Assign variables based on return statements
    if keymode == 'enter':
        RGBLed.color = Color('white')
        trycode, keymode = enterKey(key, trycode, keymode)
    else:
        RGBLed.color = Color('blue')
        trycode, keymode, KEY = newKey(key, trycode, keymode, KEY)
    screen.text(trycode, 2)

    RGBLed.color = (0, 0, 0)
    
    # Trip trigger system
    if triggerCount == 3:
        RGBLed.color = Color('red')
        screen.text('Limit Reached', 1)
        screen.text('', 2)
        buzzer.beep()

# Functions for main program to utilize
def main():

    # Function to run on key press (argument provided)
    keypad.registerKeyPressHandler(tryKey)
    Thread(target=startTimer, daemon=True).start()

def close():
    keypad.cleanup()

# Standard test program, not to be used for main functionality — refer to main file (main.py)
if __name__ == '__main__':
    try:
        main()
        pause()
    except KeyboardInterrupt:
        close()
        print('\nExited Program')
