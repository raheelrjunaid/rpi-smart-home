# Door System on Raspberry Pi 3
# Author: Raheel Junaid
# Date Started: 1/27/21

import RPi.GPIO as GPIO
from gpiozero import Servo, Buzzer, DigitalOutputDevice
from signal import pause
from multiprocessing import Process
import time
from mfrc522 import SimpleMFRC522

# IMPORTANT NOTICE: Run as "sudo" to avoid Authentication Error

rfid = SimpleMFRC522()
timerStateInput = DigitalOutputDevice(26)
servo = Servo(18, 1)
buzzer = Buzzer(17)

def triggerTimer():
    count = 0

    while True:

        if timerStateInput.value == 1:
            print('Thank you. Stopping timer process on next read.')
            break
        
        if count <= 10:
            print(("You have " + str(10 - count) + " seconds remaining\r"), end="")
            count += 1
            buzzer.beep(0.1, 0.1, n=1)
            time.sleep(1)

        else:
            break
    
    if count >= 10:
        print('Contact System Administrator to Disable')
        servo.max()
        buzzer.beep()
        pause()

timer_thread = Process(target=triggerTimer)
authUserIDs = [248227650093]
log = []

try:
    while True:

        if timerStateInput.value == 1:
            print('Timer Stopped')
            log = []
            timerStateInput.value = 0
            timer_thread.terminate()

        authenticated = False
        id, text = rfid.read()
        log.append(id)

        if len(log) > 2:
            log.pop(0)

        if (len(log) > 1 and log[-1] != log[-2]) or len(log) == 1:
            buzzer.beep(0.2, 0.2, n=1)

            for userID in authUserIDs:
                if id == userID:
                    authenticated = True

            if not timer_thread.is_alive():
                if authenticated == True:
                    servo.min() # Open Door (servo)
                    print('Authenticated\nTimer started => Disable system using Key Pad')
                    timer_thread = Process(target=triggerTimer)
                    timer_thread.start()
                else:
                    servo.max()
                    print('Authentication Error')
        
except KeyboardInterrupt:
    log = []
    servo.max()
    GPIO.cleanup() # For RFID reader only
    print('\nExited Loop')
