from gpiozero import DistanceSensor
from time import sleep

# Standard test program, not to be used for main functionality — refer to main file (main.py)
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print('\nExited Program')
