# Micropython module for the DVR8825 Stepper Driver

This is a micropython module for the designed to be used with the **DVR8825 stepper driver**.
However, I assume it could be used with similar drivers.

This module is based off of https://github.com/pedromneto97/AccelStepper-MicroPython/blob/master/AccelStepper.py and https://github.com/NikodemBartnik/Pico-Plotter/tree/main/Pico%20script.
## Module Functions

- `check_limit_swithces(pins = [ ]) -> bool`: checks if any limit switches have been triggered.
  - `pins` is a list of 'Pin' Objects (from machine in micropython).
  - If no Pins are provided, function will always return `False`.
  - Returns `True` if any switches are HIGH, `False` if any are LOW.

- `

## Class Description

```
stepper1 = Basic_Stepper(dir_pin=4,
                        step_pin=5,
                        enable_pin=6,
                        full_step_angle=1.8,
                        limit_pins=[limit_switch1]
                        )
```

### Parameters:

- `dir_pin`: pin number used for direction pin.
- `step_pin`: pin numbser used for step pin.
- `enable_pin`: pin number used for the enable pin.
- `full_step_angle`: phase angle in full mode in degrees.
  
  
  *Optional Parameters:*
- `limit_pins`: (default [ ]) list of input Pin objects used for limit switches.
- `step_mode`: (default 1) microstep modes, 1 - full, 1/2 - half, 1/4, 1/8, 1/16, 1/32.


## Class Methods
- `enable()`: Enables motor to operating state.
  
- `disable()`: Disables motor from operating state.
  
- `set_speed(s)`: Sets the speed.
  - `s` is the speed in steps/seconds in integer values.
  
- `set_direction(dir)`: Sets the direction of the motor
  - `dir` is the direction represent as an integer,
  - 0 - CCW for Counter-Clockwise, 1 - CW for Clockwise.
  
- `one_step()`: Function to make motor take a single step.
  - Takes a single step in the direction defined by the class.
  
- `move_to_absolute(absolute)`: Function to move to a given point with reference to 0.
  - `absolute` is an integer value of a point in steps, with reference to 0.
  
- `move_to_relative(relative)`: Function to move to a given point with reference to the current position.
  - `relative` is an integer value of a point in steps, with reference to the current point.

- `move_steps(steps) -> bool`: Function to take N number of steps.
  - `step` is a integer number of steps to perform.
  - breaks loop with a limit switch is set HIGH, (see class parameter `limit_pins`).


## Example 

**Coming Soon...**