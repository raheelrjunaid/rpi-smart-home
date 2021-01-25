from gpiozero import Servo, Buzzer, RGBLED
from rpi_lcd import LCD

armed = True
servo = Servo(18, 1)
RGBLed = RGBLED(27, 23, 25)
screen = LCD()
systems = {
    'fan': 1,
    'servo': 1,
    'keypad': 1,
}
buzzer = Buzzer(4)

def armSystem():
    # Arm all systems
    for system in systems:
        systems[system] = 1

    global armed
    armed = True
    servo.max()

def disarmSystem():
    # Arm all systems
    for system in systems:
        systems[system] = 0
    
    global armed
    armed = False

def readSystems(line):
    cat_string = ''
    if line == 1:
        for system in systems:
            cat_string += system[0].upper()
    else:
        for system in systems:
            status = systems[system]
            if status == 1:
                cat_string += 'T' # True
            else:
                cat_string += 'F' # False
    return cat_string

def showSystemStatus():
    screen.text(f'Systems {(len(systems) + 1) * "-"} ' + readSystems(1), 1)
    screen.text(f'Status {(len(systems) + 2) * "-"} ' + readSystems(2), 2)
