# Global Variables and Components
# Author: Raheel Junaid
# Date Started: 1/24/21

from gpiozero import Servo, Buzzer, RGBLED, DigitalOutputDevice, LED
from dotenv import load_dotenv
from gpiozero.pins.pigpio import PiGPIOFactory
import os
from rpi_lcd import LCD

load_dotenv()

try:
    remote_factory = PiGPIOFactory(host=os.environ['REMOTEPI'])
except:
    print(f'Could not connect to Raspberry Pi at {os.environ["REMOTEPI"]}')

camLED = LED(24)
servo = Servo(18, 1, pin_factory=remote_factory)
RGBLed = RGBLED(27, 23, 25)
screen = LCD()

systems = {
    'fan': "T",
    'servo': "T",
    'keypad': "T",
    'camera': "T",
    'sensor': "T",
}

buzzer = Buzzer(4)
remote_buzzer = Buzzer(17, pin_factory=remote_factory)
fan = DigitalOutputDevice(22, pin_factory=remote_factory)

def armSystem():
    # Arm all systems
    for system in systems:
        systems[system] = "T"

    remote_buzzer.off()
    servo.max()

def disarmSystem():
    # Disarm all systems
    for system in systems:
        systems[system] = "F"
    
    screen.clear()
    fan.off()
    remote_buzzer.off()

def readSystems(line):
    cat_string = ''

    # Line to print on LCD Screen
    # First is system
    if line == 1:
        for system in systems:
            cat_string += system[0].upper()

    # Second is status
    else:
        for system in systems:
            status = systems[system]
            cat_string += systems[system]

    return cat_string

def showSystemStatus():
    screen.text(f'Systems {(7 - len(systems)) * "-"} ' + readSystems(1), 1)
    screen.text(f'Status {(8 - len(systems)) * "-"} ' + readSystems(2), 2)
