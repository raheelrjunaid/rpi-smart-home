from global_vars import screen, systems, servo
from gpiozero import DigitalOutputDevice, LED, RGBLED
from colorzero import Color
import keypad
from time import sleep
from signal import pause

fan = DigitalOutputDevice(17)
RGBLed = RGBLED(27, 23, 25)

def readSystems(line):
    cat_string = ''
    if line == 1:
        for system in systems:
            cat_string += system[0].upper()
    else:
        for system in systems:
            status = systems[system]
            if status == 1:
                cat_string += 'T' # True
            else:
                cat_string += 'F' # False
    return cat_string


try:
    keypad.main()
    fan.on()
    screen.text(f'Systems {(len(systems) + 1) * "-"} ' + readSystems(1), 1)
    screen.text(f'Status {(len(systems) + 2) * "-"} ' + readSystems(2), 2)
    pause()
except KeyboardInterrupt:
    # FIX(Maybe) Module has trouble cleaning up with this function but the main function still works
    # keypad.close()
    screen.clear()
    print('\nExited Program')
