from gpiozero import DigitalOutputDevice
import keypad
from time import sleep
from signal import pause

fan = DigitalOutputDevice(17)

try:
    keypad.main()
    
    while True:
        fan.on()
        sleep(1)
    pause()
except KeyboardInterrupt:
    # FIX(Maybe) Module has trouble cleaning up with this function but the main function still works
    # keypad.close()
    print('\nExited Program')
