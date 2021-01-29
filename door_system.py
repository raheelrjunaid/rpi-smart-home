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
    count = 0 # Current countdown in seconds
    for count in range(11):
        
        # Interrupt countdown if signal is recieved from keypad (main.py)
        if timerStateInput.value == 1:
            print('Thank you. Stopping timer process on next read.')
            break
        
        # Beep every 1 second
        print(("You have " + str(10 - count) + " seconds remaining\r"), end="")
        buzzer.beep(0.1, 0.1, n=1)
        time.sleep(1)
    
    # Only execute this code if the for loop has been completed
    if count >= 10:
        print('Contact System Administrator to Disable')
        servo.max()
        buzzer.beep()
        pause() # Countinuously beep forever

timer_thread = Process(target=triggerTimer)
authUserIDs = [248227650093]
log = []

try:
    while True:

        # Reset timer on next read
        if timerStateInput.value == 1:
            print('Timer Stopped')
            log = [] # Reset log so duplicate entry is allowed
            timerStateInput.value = 0
            timer_thread.terminate()

        # Reset authentication status
        authenticated = False

        # Read data from RFID Reader 
        # This is why the while loop only executes as this function waits for data
        id, text = rfid.read()
        log.append(id)

        # Ensure the list remains only 2 entries long
        if len(log) > 2:
            log.pop(0)

        # Only execute if it is not a duplicate reading or if there is only 1 reading
        if (len(log) > 1 and log[-1] != log[-2]) or len(log) == 1:
            buzzer.beep(0.2, 0.2, n=1)

            # Compare all stored authenticated user id's to the present user ID
            for userID in authUserIDs:
                if id == userID:
                    authenticated = True

            # Only execute if the alarm hasn't been tripped
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
    log = [] # Reset Log
    servo.max() # Close the door
    buzzer.off() # Silence Alarm
    GPIO.cleanup() # For RFID reader only

    print('\nExited Loop')
