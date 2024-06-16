# Micropython module for the DVR8825 Stepper Driver

This is a micropython module for the designed to be used with the **DVR8825 stepper driver**.
However, I assume it could be used with similar drivers.

This module is based off of https://github.com/pedromneto97/AccelStepper-MicroPython/blob/master/AccelStepper.py and https://github.com/NikodemBartnik/Pico-Plotter/tree/main/Pico%20script.

  

## Module Functions

To import function(s) use: `from steppers import [function name, ...]`


- `check_limit_swithces(pins = [ ]) -> bool`: checks if any limit switches have been triggered.
  - `pins` is a list of 'Pin' Objects (from machine in micropython).
  - If no Pins are provided, function will always return `False`.
  - Returns `True` if any switches are HIGH, `False` if any are LOW.

## Class Description


```Py
import steppers

stepper1 = steppers.Basic_Stepper(
                        dir_pin=4,
                        step_pin=5,
                        enable_pin=6,
                        step_mode=1
                        )
```

### Parameters:

- `dir_pin`: pin number used for direction pin.
- `step_pin`: pin numbser used for step pin.
- `enable_pin`: pin number used for the enable pin.
  
  
  *Optional Parameters:*
- `step_mode`: (default 1) microstep modes, 1 - full, 1/2 - half, 1/4, 1/8, 1/16, 1/32.


## Class Methods
- `enable()`: Enables motor to operating state.
  
- `disable()`: Disables motor from operating state.
  
- `set_max_speed(steps_per_sec)`: Sets the speed.
  - `s` is the speed in steps/seconds in integer values.
  
- `set_direction(dir)`: Sets the direction of the motor
  - `dir` is the direction represent as an integer,
  - 0 - CCW for Counter-Clockwise, 1 - CW for Clockwise.
  
- `one_step()`: Function to make motor take a single step.
  - Takes a single step in the direction defined by the class.

- `move_steps(self, steps: int, condition_func=None, condition_params=None) -> None`: Function to take N number of steps.
  - steps: number of steps to take.
  - condition_func: function to test some condition to stop motors.
  - condition_params: parameters to be passed to the condition function.
