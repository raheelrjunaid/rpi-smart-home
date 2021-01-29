from gpiozero import MotionSensor
from datetime import datetime
from global_vars import camLED
from picamera import PiCamera
from multiprocessing import Process
from time import sleep

pirMotionSensor = MotionSensor(5)
camera = PiCamera(resolution=(1280, 720))

def newRecording():
    camera.start_recording("./cam_videos/" + datetime.now().strftime('%m.%d.%Y-%H:%M:%S') + ".h264")
    print('Recording')
    camera.wait_recording(10)
    camera.stop_recording()
    print('Finished Recording')

# Standard test program, not to be used for main functionality — refer to main file (main.py)
try:

    while True:
        
        if pirMotionSensor.value == 1:
            newRecording()

        # Represents recording duration sensitivity
        sleep(2)

except KeyboardInterrupt:
    camera.close()
    print('\nExited Program')
