# RPI Keypad Function
# Author: Raheel Junaid
# Date Started: 1/23/21

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

    # Import globals (required as function doesn't allow args)
    global trycode
    global keymode
    global KEY

    trycode += str(key)
    print(trycode, keymode)

    # Working key attempt function
    def enterKey(key, trycode, keymode):

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
                else:
                    print('failure')
                trycode = ''

        # return values to change (no global var writing)
        return trycode, keymode

    # Working change keycode function
    def newKey(key, trycode, keymode, KEY):

        # Beginning prompt
        if len(trycode) == 0:
            print('Input 4 digit code')

        # Read code change and apply change to global KEY (not global)
        elif len(trycode) == 4:
            KEY = trycode
            trycode = ''
            keymode = 'enter'

        # return values to change (no global var writing)
        return trycode, keymode, KEY

    # Runtime statement using global keymode
    # Assign variables based on return statements
    if keymode == 'enter':
        trycode, keymode = enterKey(key, trycode, keymode)
    else:
        trycode, keymode, KEY = newKey(key, trycode, keymode, KEY)

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
