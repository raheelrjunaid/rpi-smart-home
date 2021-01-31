# ADC + 7 Segment Display control using potentiometer
# Author: Raheel Junaid
# Date Started: 1/30/21

from global_vars import fan, remote_factory, showSystemStatus, systems
from gpiozero import LEDBoard
from smbus import SMBus
from time import sleep

bus = SMBus(1)

layouts = {
    '1': (False, True, True, False, False, False, False),
    '2': (True, True, False, True, True, False, True),
    '3': (True, True, True, True, False, False, True),
    '4': (False, True, True, False, False, True, True),
    '5': (True, False, True, True, False, True, True),
    '6': (True, False, True, True, True, True, True),
    '7': (True, True, True, False, False, False, False),
    '8': (True, True, True, True, True, True, True),
    '9': (True, True, True, True, False, True, True),
    '0': (True, True, True, True, True, True, False)
}

# Inspired from a function at https://www.youtube.com/watch?v=BdmQcayG8Gg
def read_ads7830():
    # Hexadecimal ID of i2c device is 4b or 0x4b
    bus.write_byte(0x4b, 0x84)
    return bus.read_byte(0x4b)

# 7 Segment Display Initialization
# Params: A, B, C, D, E, F, G, pin_factory
leds = LEDBoard(12, 19, 6, 5, 13, 16, 24, pin_factory=remote_factory)

def main():
    while True:
        value = int(read_ads7830() / 254 * 10)

        for led in range(7):
            if value != 10:
                if layouts[str(value)][led] == False:
                    leds.on(led)
                else:
                    leds.off(led)

        # Show potentiometer output
        if read_ads7830() == 0:
            fan.off()
            systems['fan'] = "F"
            if systems['fan'] != "F":
                showSystemStatus()
        else:
            fan.on()
            systems['fan'] = "T"
            if systems['fan'] != "T":
                showSystemStatus()

# Standard test program, not to be used for main functionality — refer to main file (main.py)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        leds.close()
        print('\nExited Program')
