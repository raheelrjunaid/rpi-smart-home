# RPi Smart Home Main Program
# Author: Raheel Junaid
# Date Started: 1/20/21

from global_vars import disarmSystem, showSystemStatus, armSystem
import keypad
import os
from threading import Thread
from colorzero import Color
from time import sleep
from signal import pause

try:
    keypad.main() # "keypad" Required to avoid circular import
    armSystem()
    showSystemStatus()
    pause()
except KeyboardInterrupt:
    # FIX(Maybe) Module has trouble cleaning up with this function but the main function still works
    # keypad.close()

    print('\nShutting Down Systems...')
    disarmSystem()
    print('Exited Program')