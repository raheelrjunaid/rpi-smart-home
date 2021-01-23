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

ROW_PINS = [4, 17, 27, 22]
COL_PINS = [5, 6, 13, 19]

factory = rpi_gpio.KeypadFactory()

keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

def printKey(key):
    print(key)

def main():
    keypad.registerKeyPressHandler(printKey)
def close():
    keypad.cleanup()

if __name__ == '__main__':
    try:
        main()
        pause()
    except KeyboardInterrupt:
        close()
        print('\nExited Program')
