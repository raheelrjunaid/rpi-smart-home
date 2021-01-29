from gpiozero import MotionSensor
from datetime import datetime
from threading import Thread
from global_vars import camLED, systems, showSystemStatus
from picamera import PiCamera
from time import sleep, time

pirMotionSensor = MotionSensor(5)
camera = PiCamera(resolution=(1280, 720))
repeat = True

def newRecording(tripped_alarm=False):
    global repeat

    if tripped_alarm:
        camera.start_recording("./cam_videos/Breakin" + datetime.now().strftime('%m.%d.%Y-%H:%M:%S') + ".h264", splitter_port=2)
    else:
        camera.start_recording("./cam_videos/Rec" + datetime.now().strftime('%m.%d.%Y-%H:%M:%S') + ".h264")
    print('Recording')
    startTime = time()

    camLED.on()
    systems['camera'] = "R"
    showSystemStatus()

    if tripped_alarm:
        while True:
            camera.wait_recording(10, splitter_port=2)
    else:
        while repeat:
            repeat = False
            camera.wait_recording(10)
        
    camera.stop_recording()
    print(f'Finished {int(time() - startTime)}s Recording.\n{20 * "="}')

    if not camera.recording:
        camLED.off()

    systems['camera'] = "T"
    showSystemStatus()

def main():
    global repeat

    while True:
        if pirMotionSensor.value == 1:
            print('Motion Detected')
            repeat = True

            if camera.recording:
                print('repeat sent')
            else:
                Thread(target=newRecording, daemon=True).start()

        sleep(2)

# Standard test program, not to be used for main functionality — refer to main file (main.py)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        camera.close()
        print('\nExited Program')
