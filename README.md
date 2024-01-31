# Micropython module for the DVR8825 Stepper Driver

This is a micropython module for the DVR8825 stepper driver.

This is based off of https://github.com/pedromneto97/AccelStepper-MicroPython/blob/master/AccelStepper.py and https://github.com/NikodemBartnik/Pico-Plotter/tree/main/Pico%20script.

## Class Description

`stepper1 = Stepper(0, 1, 2, mode_pins=(3, None, None), step_mode='1/2')`

Parameters:
- `steps_per_rev`: number of steps per revolution in "FULL" step mode (default 200).
- `dir_pin`: pin used for dir.
- `step_pin`: pin used for step.
- `enabled`: pin used for enable.
  
  Optional Parameters
- `mode_pins`:  pins for M0, M1, M2 (default (None, None, None)).
- **More To Come**






## Example 

**Coming Soon...**