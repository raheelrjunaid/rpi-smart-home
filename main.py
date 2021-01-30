# RPi Smart Home Main Program
# Author: Raheel Junaid
# Date Started: 1/20/21

from global_vars import disarmSystem, showSystemStatus, armSystem, screen
import keypad, camera_pir, os, furnace_adc
from threading import Thread
from colorzero import Color
from time import sleep
from signal import pause

try:
    keypad.main() # "keypad" Required to avoid circular import
    # furnace_adc.main()
    armSystem()
    showSystemStatus()
    camera_pir.main()
    pause()
except KeyboardInterrupt:
    # FIX(Maybe) Module has trouble cleaning up with this function but the main function still works
    # keypad.close()

    camera_pir.camera.close()
    # furnace_adc.leds.close()
    print('\nShutting Down Systems...')
    screen.clear()
    disarmSystem()
    print('Exited Program')
