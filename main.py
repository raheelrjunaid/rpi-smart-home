# RPi Smart Home Main Program
# Author: Raheel Junaid
# Date Started: 1/20/21

from global_vars import disarmSystem, showSystemStatus, armSystem, screen, remote_buzzer, fan
import keypad, camera_pir, os, furnace_adc
from threading import Thread, enumerate
from time import sleep, time
from signal import pause

def monitorThreads():
    while True:
        print("-" * 20)
        for thread in enumerate():
            print(thread.name)
        print("-" * 20)
        sleep(3)

threads = [
    Thread(name="ADC", target=furnace_adc.main, daemon=True),
    Thread(name="KeypadTimeout", target=keypad.startTimer, daemon=True),
    Thread(name="Camera", target=camera_pir.main, daemon=True)
]

try:
    keypad.keypad.registerKeyPressHandler(keypad.tryKey)
    
    for thread in threads:
        thread.start()

    if os.environ['DEVMODE'] == "True":
        Thread(name="Monitoring", target=monitorThreads, daemon=True).start()

    armSystem()
    showSystemStatus()
    pause()
except KeyboardInterrupt:
    print('\nShutting Down Systems...')
    # Show timer
    startTime = time()

    for thread in threads:
        # Allow threads to end processess
        print(("-" * 20) + "\nWaiting for " + thread.name + "\n" + ("-" * 20), (len(threads) * 10) - int(time() - startTime) + "seconds remaining")
        # Warn user of closing exceptions
        if threads.index(thread) == len(threads) - 1:
            print('On the last thread, Error may return')
        thread.join(5)

    # Close down all optional systems
    screen.clear()

    # Remote systems need to be closed instead of turned off
    remote_buzzer.close()
    fan.close()

    # Close down all mandatory systems
    furnace_adc.leds.close()
    camera_pir.camera.close()
    disarmSystem()

    print('\nExited Program')
