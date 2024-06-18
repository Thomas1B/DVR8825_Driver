# Micropython module for the DVR8825 Stepper Driver

This is a micropython module for the designed to be used with the **DVR8825 stepper driver**.
However, I assume it could be used with similar drivers. This class is a based of [this](https://how2electronics.com/control-stepper-motor-with-drv8825-raspberry-pi-pico/) article.

Note: Arduinos are better for motor controls due to real-time performance. The [AccelStepper](http://www.airspayce.com/mikem/arduino/AccelStepper/) is a great library to use.

## Module Functions

To import function(s) use: `from steppers import [function name, ...]`


- `check_limit_swithces(pins = [ ]) -> bool`: checks if any limit switches have been triggered.
  - `pins` is a list of 'Pin' Objects (from machine in micropython).
  - If no Pins are provided, function will always return `False`.
  - Returns `True` if any switches are HIGH, `False` if any are LOW.

## Class Description

Stay tuned!!!