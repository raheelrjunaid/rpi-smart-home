# RPI Keypad Function
# Author: Raheel Junaid
# Date Started: 1/23/21

from global_vars import buzzer, screen
from time import sleep
from pad4pi import rpi_gpio
from signal import pause

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

# TODO Change to *user environment variable
KEY = '1234'

keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

# Default Key Mode
keymode = 'enter'
trycode = ''

def tryKey(key):
    buzzer.beep(0.2, n=1)

    # Import globals (required as function doesn't allow args)
    global trycode
    global keymode
    global KEY

    trycode += str(key)
    print(trycode, keymode)

    # Working key attempt function
    def enterKey(key, trycode, keymode):
        screen.text('Attempt', 1)

        # Reset Code
        if key == '*':
            trycode = ''
            print('reset code') # TODO Also make this key arm security system

        # Change key mode to begin changing keycode
        elif key == '#':
            trycode = ''
            keymode = 'change'
            newKey(key, trycode, keymode, KEY)

        # Read code attempt and compare to actual KEY
        else:
            if len(trycode) == 4:
                if trycode == KEY:
                    print('success') # TODO Disarm security system
                    screen.text('Attempt Passed', 1)
                    screen.text('', 2)
                    buzzer.beep(0.1, 0.1, n=2)
                    sleep(1)
                else:
                    print('failure')
                    buzzer.beep(0.1, 0.1, n=3)
                    screen.text('Attempt Failed', 1)
                    screen.text('', 2)
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
            KEY = trycode
            screen.text(f'to {trycode}', 2)
            trycode = ''
            keymode = 'enter'
            sleep(1)
            screen.text('Attempt', 1)
            buzzer.beep(0.2, 0.1, n=3)

        # return values to change (no global var writing)
        return trycode, keymode, KEY

    # Runtime statement using global keymode
    # Assign variables based on return statements
    if keymode == 'enter':
        trycode, keymode = enterKey(key, trycode, keymode)
    else:
        trycode, keymode, KEY = newKey(key, trycode, keymode, KEY)
    screen.text(trycode, 2)

# Functions for main program to utilize
def main():
    # Function to run on key press (argument provided)
    keypad.registerKeyPressHandler(tryKey)

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
