from gpiozero import AngularServo, Buzzer

servo = AngularServo(18, 90, min_pulse_width=0.16/1000, max_pulse_width=2/1000)
buzzer = Buzzer(4)
