'''

Written 2024

Micropython module for the DVR8825 Stepper motor drive to used with the Pi Pico.


'''

import utime
from machine import Pin


# Constants
STEP_PER_MM = 80
MM_PER_STEP = 1 / STEP_PER_MM


class Stepper:
    '''
    Class to be used with DVR8825 stepper driver.

    Parameters:
        dir_pin: pin used for dir.
        step_pin: pin used for step.
        enabled: pin used for enable.

        # Optional
        mode_pins:  pins for M0, M1, M2 (default (None, None, None)).
        step_mode: what step micro-step per phase to use ('FULL', '1/2', '1/4', '1/8', '1/16', '1/32') (default - 'FULL').
        steps_per_rev: number of steps per revolution in "FULL" step mode, (default 200).
    '''

    def __init__(self,
                 dir_pin,  # Dir pin
                 step_pin,  # step pin
                 enable_pin,  # enable pin

                 # Optional Parameters:
                 mode_pins=(None, None, None),  # Pins for M0, M1, M2
                 step_mode='FULL',
                 steps_per_rev=200,
                 ) -> None:

        # Objects for direction, step and enable pins
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.enable_pin = Pin(enable_pin, Pin.OUT)

        # Scale factors for microsteps per phase for modes
        self.microsteps = {
            'FULL': 1,
            '1/2': 2,
            '1/4': 4,
            '1/8': 8,
            '1/16': 16,
            '1/32': 32
        }

        # pin states for mode configuration
        mode_config = {
            # M0, M1, M2
            'FULL': (0, 0, 0),
            '1/2': (1, 0, 0),
            '1/4': (0, 1, 0),
            '1/8': (1, 1, 0),
            '1/16': (0, 0, 1),
            '1/32': (1, 0, 1),
        }

        # if any mode pins have been given intialize them
        if mode_pins[0]:
            self.mode0 = Pin(mode_pins[0], Pin.OUT)
            self.mode0.value(mode_config[step_mode])
        if mode_pins[1]:
            self.mode1 = Pin(mode_pins[1], Pin.OUT)
            self.mode0.value(mode_config[step_mode])
        if mode_pins[2]:
            self.mode0.value(mode_config[step_mode])
            self.mode2 = Pin(mode_pins[2], Pin.OUT)
            self.mode2.value(mode_config[2])

        self._enable = False  # motor running _enable
        self.disable()

        # self.delay = .005/microsteps[step_mode]  # default delay for stepping
        self.delay = 20  # default delay for stepping
        self.step_mode = step_mode
        self.step_per_rev = steps_per_rev

    def enable(self) -> None:
        '''
        Function to enable the motor.

            motor is ready.
        '''
        self.enable_pin.value(0)
        self._enable = True
        utime.sleep_ms(10)

    def disable(self) -> None:
        '''
        Function to enable the motor.

            motor is free.
        '''
        self.enable_pin.value(1)
        self._enable = False

    def move_steps(self, direction: str, step_count: int, delay=0) -> None:
        '''
        Function to move a given number of steps in a certain direction.

        Parameters:
            direction: 'forward' - counter clockwise, 'backward' - clockwise
            step_count: how many steps to take.
            delay (default 0): delay time (microseconds) for adjsuting speed.
        '''

        if self._enable is False:
            raise ValueError("Motors must be enable to step.")

        if step_count < 0:
            raise ValueError('Parameter "step_count" must be greater than 0.')

        if type(delay) is not int:
            raise ValueError(f'Parameter "delay" must be an integer.')

        while step_count > 0:
            step_count -= 1
            if direction == 'forward':
                self.dir_pin.value(0)
            elif direction == 'backward':
                self.dir_pin.value(1)

            self.step_pin.value(0)
            utime.sleep_us(1)
            self.step_pin.value(1)
            utime.sleep_us(400 + delay)

    def revolution(self, rev_count, direction='forward', delay=0):
        '''
        Function to spin a given number of complete revolution
        '''

        steps_per_rev = rev_count*self.step_per_rev * \
            self.microsteps[self.step_mode]
        self.move_steps(
            direction=direction,
            step_count=steps_per_rev,
            delay=delay
        )

    def stop(self):
        '''
        Function to stop motor.
        '''
        self.step_pin.value(0)


if __name__ == "__main__":

    # Creating stepper object
    stepper1 = Stepper(
        dir_pin=0,
        step_pin=1,
        enable_pin=2,
        mode_pins=(3, None, None),
        step_mode='1/2')

    delay = 1000  # delay time in ms

    try:

        stepper1.enable()

        while True:
            stepper1.move_steps('forward', 200, delay=0)
            utime.sleep_ms(delay)
            stepper1.move_steps('backward', 200, delay=0)
            utime.sleep_ms(delay)

    except KeyboardInterrupt:
        stepper1.disable()
