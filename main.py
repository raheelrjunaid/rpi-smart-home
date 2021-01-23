from gpiozero import DigitalInputDevice
from time import sleep

Line1 = DigitalInputDevice(4)
Line2 = DigitalInputDevice(17)
Line3 = DigitalInputDevice(27)
Line4 = DigitalInputDevice(22)
Col1 = DigitalInputDevice(5)
Col2 = DigitalInputDevice(6)
Col3 = DigitalInputDevice(13)
Col4 = DigitalInputDevice(19)

try:
    while True:
        print(Line1.value)
        sleep(0.5)
except KeyboardInterrupt:
    print('\n\nExited Program\n')
