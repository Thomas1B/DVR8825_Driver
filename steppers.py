'''
Written 2024

Micropython module for the DVR8825 Stepper motor drive to used with the Pi Pico.

Rotation Directions:
    - Positive steps rotate counter-clockwise (CCW) to the left.
    - Negative steps rotate clockwise (CW) to the right.
'''

import utime
from machine import Pin


# ************** User Parameters *************
STEPS_PER_MM = 30


# ************** System Parameters *************

CCW = 0  # Counter-Clockwise.
CW = 1  # Clockwise.
MM_PER_STEP = 1/STEPS_PER_MM


HIGH = 1
LOW = 0

# ************** Functions *************


def check_limit_switches(pins=[]) -> bool:
    '''
    Function used to check if a limit switch has been triggered.
        Pins are HIGH if triggered.

    Parameters:
        pins (optional): list of input Pin objects used for limit switches.

    Returns:
        True if any limit switch is triggered, False if not.
    '''

    if type(pins) is not list:
        raise TypeError("The parameter 'pins' needs to be a list.")

    if not all(isinstance(pin, Pin) for pin in pins):
        raise ValueError(
            "Parameter \"pins\" needs be a list of pin objects, [Pin], or left empty, [].")

    if pins:  # checking there is at least one Pin object
        results = [True if pin.value() == HIGH else False for pin in pins]
        results = True if any(results) else False
        return results
    else:
        return False


def constrain(val, min_val, max_val):
    '''
    Function to contrain a value between 2 other values

    Parameters:
        val: value to constrain.
        min_val: minimum allowed value.
        max_val: maximum allowed value.

    Returns:
        float of contrained value.
    '''

    # Works by take largest of the minimum allowed value and given value,
    # then taking the smallest of that result and the maximum allowed.
    return min(max_val, max(min_val, val))


class Basic_Stepper:
    '''
    Class for stepper motor control using a DVR8825 Stepper Driver.

    Parameters:
        dir_pin: pin number used for direction pin.
        step_pin: pin numbser used for step pin.
        enable_pin: pin number used for the enable pin.
        full_step_angle: phase angle in full mode in degrees.
        step_mode (default 1): microstep modes, 1 - full, 1/2 - half, 1/4, 1/8, 1/16, 1/32.
        limit_pins (default []): list of input Pin objects used for limit switches.
    '''

    def __init__(self,
                 dir_pin: int,  # direction pin #.
                 step_pin: int,  # step pin #.
                 enable_pin=None,  # enable pin #.
                 full_step_angle=1.8,  # phase angle in full mode in degrees.
                 step_mode=1,  # 1, 1/2, 1/4, 1/8, 1/16, 1/32,
                 # limit_pins: list of input Pin objects used for limit switches.
                 limit_pins=[]
                 ) -> None:

        self._limit_pins = [pin for pin in limit_pins]

        self._step_mode = step_mode  # what microstepping mode.
        self.steps_per_rev = 360/full_step_angle  # steps per revolution.
        self._direction = CCW

        # Pin objects for direction, step and enable
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.enable_pin = Pin(enable_pin, Pin.OUT) if enable_pin else None

        self.enabled = False  # operating state of motor
        self.disable()

        self._lastStepTime = 0
        self._step_interval = 0  # microseconds/step
        self._steps_per_sec = 0  # steps/sec
        self._current_pos = 0  # in steps
        self._target_pos = 0  # in steps, negative steps to the left.

    def enable(self) -> None:
        '''
        Function to enable the motor for operation.
        '''
        self.enabled = True
        if self.enable_pin:
            self.enable_pin.value(LOW)
            utime.sleep_ms(50)

    def disable(self) -> None:
        '''
        Function to disable the motor from operation.
        '''

        self.enabled = False
        if self.enable_pin:
            self.enable_pin.value(HIGH)

    def set_speed(self, s) -> None:
        '''
        Function to set the motors speed in steps/second.

        Parameters:
            s: speed of motor in steps/second.
        '''

        if s == 0:
            self._step_interval = 0
            self._steps_per_sec = 0

        else:
            # Calculating delay time between each step in microseconds (delay/step).
            # 1e6 convert seconds to microseconds.
            delay = abs(1e6/s)
            self._step_interval = round(delay)  # microseconds/step

            self._steps_per_sec = s

    def set_direction(self, dir: int):
        '''
        Function to set the direcion of the motor.

        Parameters:
            dir: direction motor spins, 0, 1
        '''
        if dir not in [CCW, CW]:
            raise ValueError(
                'Direction must be either the integer "0" or "1".')

        if dir == CCW:
            self._direction = CCW
            self.dir_pin.value(CCW)
        else:
            self._direction = CW
            self.dir_pin.value(CW)

    def one_step(self) -> None:
        '''
        Function to take one step.
        '''

        if self._current_pos == self._target_pos:
            # if the current position is already at the targer position no nothing
            return

        if self.enabled is False:
            raise ValueError(
                "A motor is disabled, call '.enable()' to enable it, motors need to be enabled before operating."
            )

        if self._step_interval <= 0:
            self.disable()
            raise ValueError((
                "Stepper needs a speed, call .set_speed() to set a speed before operating."
            ))

        self.step_pin.value(0)
        self.step_pin.value(1)

        if self._direction == CCW:
            self._current_pos += 1
        else:
            self._current_pos -= 1

        print(self._current_pos)

    def move_to_absolute(self, absolute: int) -> None:
        '''
        Function to move to an absolution position.

        Parameters:
            absolute: absolute position in steps from home position.
        '''

        if self._target_pos != absolute:
            self._target_pos = absolute
            self.move_steps(self.steps_to_target())

    def move_to_relative(self, relative: int) -> None:
        '''
        Function to move to a point relative to the current position.

        Parameters:
            relative: relative position in steps
        '''
        self.move_to_absolute(self._current_pos + relative)

    def move_steps(self, steps: int) -> bool:
        '''
        Function to move motor a certain number of steps.
            - If checK_limit_switches() return True, motor stop.

        Parameters:
            steps: + steps is CCW, - steps is CW.
        '''

        # Positive steps rotate counter-clockwise.
        # Negative steps rotate clockwise.
        direction = CCW if steps > 0 else CW
        self.set_direction(direction)

        # Performing a step of N of total steps every time the current time
        # is increased by one step interval
        steps_to_do = abs(steps)
        lastread = utime.ticks_us()
        while steps_to_do > 0:
            cur_time = utime.ticks_us()
            if cur_time - lastread >= self._step_interval:
                steps_to_do -= 1
                self.one_step()
                lastread = cur_time

            if check_limit_switches(self._limit_pins):
                utime.sleep_ms(250)  # debouncing time for limit switch.F
                break

    def current_position(self) -> int:
        '''
        Function to get the current position in steps.
        '''
        return self._current_pos

    def target_position(self) -> int:
        '''
        Function to get the target position in steps.
        '''
        return self._target_pos

    def steps_to_target(self) -> int:
        '''
        Function to calculate the number of steps until to the target position.
        '''
        steps = self._target_pos - self._current_pos
        return steps


# ************************* TESTING *************************
if __name__ == '__main__':

    try:

        limit_switch1 = Pin(13, Pin.IN)

        stepper1 = Basic_Stepper(dir_pin=4,
                                 step_pin=5,
                                 enable_pin=6,
                                 full_step_angle=1.8,
                                 limit_pins=[limit_switch1]
                                 )

        stepper1.enable()

        stepper1.set_speed(700)

        stepper1.move_to_absolute(2000)
        stepper1.move_to_absolute(200)

        stepper1.disable()

    except KeyboardInterrupt:
        stepper1.disable()
