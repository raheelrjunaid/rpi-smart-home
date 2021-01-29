from gpiozero import MotionSensor
from datetime import datetime
from threading import Thread
from global_vars import camLED, systems, showSystemStatus
from picamera import PiCamera
from time import sleep, time

pirMotionSensor = MotionSensor(5)
camera = PiCamera(resolution=(1280, 720))
repeat = True

def newRecording():
    global repeat

    camera.start_recording("./cam_videos/Rec" + datetime.now().strftime('%m.%d.%Y-%H:%M:%S') + ".h264")
    print('Recording')
    startTime = time()

    camLED.on()
    systems['camera'] = "R"
    showSystemStatus()

    while repeat:
        repeat = False
        camera.wait_recording(10)
        
    camera.stop_recording()
    print(f'Finished {int(time() - startTime)}s Recording.\n{20 * "="}')

    camLED.off()
    systems['camera'] = "T"
    showSystemStatus()

recordingThread = Thread(target=newRecording, daemon=True)

def main():
    global repeat

    while True:
        if pirMotionSensor.value == 1:
            print('Motion Detected')

            if camera.recording:
                repeat = True
                print('repeat sent')
            else:
                recordingThread.start()

        sleep(2)

# Standard test program, not to be used for main functionality — refer to main file (main.py)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        camera.close()
        print('\nExited Program')
