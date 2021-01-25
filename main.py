from global_vars import servo
from gpiozero import DigitalOutputDevice, LED, RGBLED, Servo
from colorzero import Color
import keypad
from time import sleep
from signal import pause

fan = DigitalOutputDevice(17)
RGBLed = RGBLED(27, 23, 25)

try:
    keypad.main()
    fan.on()
    pause()
except KeyboardInterrupt:
    # FIX(Maybe) Module has trouble cleaning up with this function but the main function still works
    # keypad.close()
    print('\nExited Program')
