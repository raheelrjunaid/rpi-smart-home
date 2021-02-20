<h1 align="center">:house:<br>rpi-smart-home</h1>

<p align="center"><img src="https://img.shields.io/badge/Build-Passing-success"> <img src="https://img.shields.io/badge/Status-Not%20Maintained-critical"> <img src="https://img.shields.io/badge/version-1.0-blue"></p>

A smart Home security system primarily built using Python and the modern gpiozero API. It implements a variety of features such as a motion-sensor activated Camera, a Keypad, Potentiometer input, an LCD display, RFID Reader, an Angular Servo and more!

## Quick-Links
- [Wiki (About and Features)](https://img.shields.io/badge/Status-Not%20Maintained-red)

## Motivation
This project was made so I could learn more about how different files can interact with each other, and using those concepts, how I could write clean code for people to contribute to.

## Code style
The current code is a rough draft as there are some bloaded areas and confused use of Processes and Threads. The code in general is restricted through the disallowance
of necessary function parameters. These parameters would conventionally return a value to be updated, but because of the restriction, I've had to resort to the use
of global variables. Embedded functions will be normal as they are unaffected by library restrictions.

## Modules and Libraries
As mentioned, their is a heavy reliance on the gpiozero library and a light reliance on the following:

| Need to be installed | Already installed |
| - | - |
colorzero | threading
pad4pi | time
smbus | signal
dotenv (environment variables) | os (environment variables)
mfrc522 | 
rpi_lcd |
picamera |
camera_pir |

## Credits
- `furnace_adc.py`
  - "layouts" dictionary <https://www.stuffaboutcode.com/2016/10/raspberry-pi-7-segment-display-gpiozero.html>
  - "read_ads7830" function <https://www.youtube.com/watch?v=BdmQcayG8Gg>
