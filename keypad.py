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

keymode = 'enter'

trycode = ''
def tryKey(key):
    global trycode
    global keymode
    trycode += str(key)
    print(trycode)
    
    if key == '*':
        trycode = ''
        print('reset code')
    elif key == '#':
        trycode = ''
        keymode = 'change'
        newKey(0)
    else:
        if len(trycode) == 4:
            if trycode == KEY:
                print('success')
            else:
                print('failure')
            trycode = ''

def newKey(key):
    global KEY
    global trycode
    global keymode
    print('Input 4 digit code')
    trycode += str(key)
    if len(trycode) == 4:
        KEY = trycode
        trycode = ''
        keymode = 'enter'

def main():
    if keymode == 'change':
        keypad.registerKeyPressHandler(newKey)
    else:
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
