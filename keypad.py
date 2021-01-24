# RPI Keypad Function
# Author: Raheel Junaid
# Date: 1/23/21

from pad4pi import rpi_gpio
from signal import pause

KEYPAD = [
    [1, 2, 3, 'A'],
    [4, 5, 6, 'B'],
    [7, 8, 9, 'C'],
    ['*', 0, '#', 'D']
]

ROW_PINS = [12, 16, 20, 21]
COL_PINS = [6, 13, 19, 26]

factory = rpi_gpio.KeypadFactory()

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
        if key == '*':
            trycode = ''
            print('reset code')
        elif key == '#':
            trycode = ''
            keymode = 'change'
            newKey(key, trycode, keymode, KEY)
        else:
            if len(trycode) == 4:
                if trycode == KEY:
                    print('success')
                else:
                    print('failure')
                trycode = ''
        return trycode, keymode

    # Working change keycode function
    def newKey(key, trycode, keymode, KEY):
        if len(trycode) == 0:
            print('Input 4 digit code')
        elif len(trycode) == 4:
            KEY = trycode
            print(KEY)
            trycode = ''
            keymode = 'enter'
        return trycode, keymode, KEY

    if keymode == 'enter':
        trycode, keymode = enterKey(key, trycode, keymode)
    else:
        trycode, keymode, KEY = newKey(key, trycode, keymode, KEY)

def main():
    keypad.registerKeyPressHandler(tryKey)

def close():
    keypad.cleanup()

if __name__ == '__main__':
    try:
        main()
        pause()
    except KeyboardInterrupt:
        close()
        print('\nExited Program')
