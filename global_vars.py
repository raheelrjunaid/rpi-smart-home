from gpiozero import AngularServo, Buzzer
from rpi_lcd import LCD

armed = True
servo = AngularServo(18, 90)
screen = LCD()
systems = {
    'fan': 1,
    'servo': 1,
    'keypad': 1,
}
buzzer = Buzzer(4)
def armSystem():
    global armed
    armed = True
    servo.max()
