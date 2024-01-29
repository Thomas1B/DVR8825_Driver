# Micropython module for the DVR8825 Stepper Driver

This is a micropython module for the DVR8825 stepper driver.

This is based off of https://github.com/NikodemBartnik/Pico-Plotter/tree/main/Pico%20script and https://github.com/dimschlukas/rpi_python_drv8825/blob/master/example.py.

## Class Description

`stepper1 = Stepper(0, 1, 2, mode_pins=(3, None, None), step_mode='1/2')`

Parameters:
- `dir_pin`: pin used for dir.
- `step_pin`: pin used for step.
- `enabled`: pin used for enable.
  
  Optional Parameters
- `mode_pins`:  pins for M0, M1, M2 (default (None, None, None)).
- `step_mode`: what step micro-step per phase to use ('FULL', '1/2', '1/4', '1/8', '1/16', '1/32') (default - 'FULL').
- `steps_per_rev`: number of steps per revolution in "FULL" step mode (default 200).






## Example 

```py
import steppers
import utime

stepper1 = steppers.Stepper(0, 1, 2, mode_pins=(3, None, None), step_mode='1/2')

stepper1.enable() # enable motors
for _ in range(2):
    stepper1.steps('forward', 800) # 2 rotation counter-clockwise
    utime.sleep(2)
    stepper1.steps('backward', 800) # 2 rotation clockwise
    utime.sleep(2)
stepper1.disable()

```