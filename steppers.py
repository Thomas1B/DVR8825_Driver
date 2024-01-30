'''

Written 2024

Micropython module for the DVR8825 Stepper motor drive to used with the Pi Pico.


'''

import utime
from machine import Pin


# Constants
STEPS_PER_MM = 80
MM_PER_STEPS = 1 / STEPS_PER_MM


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
        microsteps = {
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

        self.state = False  # motor running state
        self.disable()

        self.step = 0  # step position

        self.delay = .005/microsteps[step_mode]  # default delay for stepping
        self.step_per_rev = steps_per_rev
        self.adj_steps_per_rev = steps_per_rev * microsteps[step_mode]

    def enable(self) -> None:
        '''
        Function to enable the motor.

            motor is ready.
        '''
        self.enable_pin.value(0)
        self.state = True
        utime.sleep_ms(10)

    def disable(self) -> None:
        '''
        Function to enable the motor.

            motor is free.
        '''
        self.enable_pin.value(1)
        self.state = False

    def move_steps(self, direction: str, step_count: int, delay=0) -> None:
        '''
        Function to move a given number of steps in a certain direction.

        Parameters:
            direction: 'forward' - counter clockwise, 'backward' - clockwise
            step_count: how many steps to take.
            delay (default 0): delay time (microseconds) for adjsuting speed.
        '''

        if self.state == False:
            raise ValueError("Motors must be enable to step.")

        if step_count < 0:
            raise ValueError('Parameter "step_count" must be greater than 0.')

        # for _ in range(step_count):
        while step_count > 0:
            step_count -= 1
            if direction == 'forward':
                self.dir_pin.value(0)
                self.step += 1
            elif direction == 'backward':
                self.step -= 1
                self.dir_pin.value(1)

            self.step_pin.value(0)
            self.step_pin.value(1)
            utime.sleep_us(300 + (delay))


if __name__ == "__main__":

    stepper1 = Stepper(0, 1, 2, mode_pins=(3, None, None),
                       step_mode='1/2')

    stepper1.enable()

    for _ in range(2):
        print(stepper1.step)
        stepper1.move_steps('forward', 4000, delay=0)
        print(stepper1.step)
        utime.sleep(2)
        stepper1.move_steps('backward', 4000, delay=500)
        print(stepper1.step)
        utime.sleep(2)

    stepper1.disable()
