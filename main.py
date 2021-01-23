import keypad
from signal import pause

try:
    keypad.main()
    pause()
except KeyboardInterrupt:
    keypad.close()
    print('\nExited Program')
