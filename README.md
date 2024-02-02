# Micropython module for the DVR8825 Stepper Driver

This is a micropython module for the designed to be used with the **DVR8825 stepper driver**.
However, I assume it could be used with similar drivers.

This module is based off of https://github.com/pedromneto97/AccelStepper-MicroPython/blob/master/AccelStepper.py and https://github.com/NikodemBartnik/Pico-Plotter/tree/main/Pico%20script.

## Module Conventions

  1. Rotation Directions:
     - Positive steps rotate counter-clockwise (CCW) to the left.
     - Negative steps rotate clockwise (CW) to the right.

  2. Speed is in steps/sec, unless specifically said.
  
  3. Distance and number of steps are in absolute positioning.

## Module Functions

To import function(s) use: `from steppers import [function name, ...]`


- `check_limit_swithces(pins = [ ]) -> bool`: checks if any limit switches have been triggered.
  - `pins` is a list of 'Pin' Objects (from machine in micropython).
  - If no Pins are provided, function will always return `False`.
  - Returns `True` if any switches are HIGH, `False` if any are LOW.

## Class Description


```
import steppers

stepper1 = steppers.Basic_Stepper(dir_pin=4,
                        step_pin=5,
                        enable_pin=6,
                        full_step_angle=1.8,
                        limit_pins=[limit_switch1],
                        step_mode=1
                        )
```

### Parameters:

- `dir_pin`: pin number used for direction pin.
- `step_pin`: pin numbser used for step pin.
- `enable_pin`: pin number used for the enable pin.
  
  
  *Optional Parameters:*
- `full_step_angle`: (default 1.8) phase angle in full mode in degrees.
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
- `current_position() -> int`: Returns the current position in number of steps.
  - when class is intialized this is set to 0.
- `target_position() -> int`: Returns the target position in number of steps.
  - when class is intialized this is set to 0.
- `steps_to_target() -> int`: Returns the number of steps from the current position to the target position.


## Example 

```py
try:

    STEPS_PER_MM = 30

    stepper1 = Basic_Stepper(dir_pin=4,
                            step_pin=5,
                            enable_pin=6,
                            full_step_angle=1.8,
                            limit_pins=[],
                            step_mode=1)

    stepper1.set_speed(700) # setting speed to 700 steps/sec

    mm = 20 
    steps = mm * STEPS_PER_MM # converting distance to number of steps.

    # Just displaying some stats
    print(f'Number of steps for {mm} mm, steps = {steps}')
    utime.sleep(3)

    stepper1.enable() # enabling motor for operation.

    stepper1.move_to_absolute(steps) # moving to an absolute point.
    utime.sleep(1) # stopping for one second.
    stepper1.move_to_relative(-steps) # moving back to previous position.

    stepper1.disable() # disabling motor from operation (save power).

except KeyboardInterrupt:
    stepper1.disable()

```