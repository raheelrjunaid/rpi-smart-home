# RPi Smart Home Main Program
# Author: Raheel Junaid
# Date Started: 1/20/21

from global_vars import screen, systems, servo, disarmSystem, showSystemStatus, RGBLed
from gpiozero import DigitalOutputDevice
from threading import Thread
from colorzero import Color
import keypad
from time import sleep
from signal import pause

fan = DigitalOutputDevice(17)
timer = 0

try:
    keypad.main()
    fan.on()
    showSystemStatus()
    pause()
except KeyboardInterrupt:
    # FIX(Maybe) Module has trouble cleaning up with this function but the main function still works
    # keypad.close()

    disarmSystem()
    showSystemStatus()
    print('\nShutting Down Systems...')

    sleep(3)
    screen.clear()
    print('Exited Program')
