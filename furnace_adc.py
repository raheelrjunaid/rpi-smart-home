from global_vars import fan
from smbus import SMBus
from time import sleep

bus = SMBus(1)

# Inspired from a function at https://www.youtube.com/watch?v=BdmQcayG8Gg
def read_ads7830():
    # Hexadecimal ID of i2c device is 4b or 0x4b
    bus.write_byte(0x4b, 0x84)
    return bus.read_byte(0x4b)

def main():
    fan.on()
    while True:
        # Show potentiometer output
        print(read_ads7830())
        sleep(0.5)

# Standard test program, not to be used for main functionality — refer to main file (main.py)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExited Program')
