from gpiozero import AngularServo, Buzzer
from rpi_lcd import LCD

servo = AngularServo(18, 90, min_pulse_width=0.16/1000, max_pulse_width=2/1000)
screen = LCD()
systems = {
    'fan': 1,
    'servo': 1,
    'keypad': 1,
}
buzzer = Buzzer(4)
