'''
Written 2024

Micropython module for the DVR8825 Stepper motor drive to used with the Pi Pico.

Rotation Directions:
    - Positive steps rotate counter-clockwise (CCW).
    - Negative steps rotate clockwise (CW).
'''

import utime
from machine import Pin


# DO NOT CHANGE
CCW = 0  # Counter-Clockwise.
CW = 1  # Clockwise.


class Stepper:
    def __init__(self,
                 step_per_rev: int,  # number of steps per revolution
                 dir_pin: int,  # direction pin #.
                 step_pin: int,  # step pin #.
                 enable_pin: int,  # enable pin #.
                 mode_pins=(None, None, None)  # mode pins (M0, M1, M2)
                 ) -> None:

        self.direction = CCW  # direction of motor: 0 - CCW, 1 - CW
        self.steps_per_rev = step_per_rev  # steps per revolution

        # direction, step and enable pin objects on Stepper Driver
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.enable_pin = Pin(enable_pin, Pin.OUT)

        self.enabled = False  # motor is ready to run
        self.disable()

        # setting default speed
        self.set_speed(75)

    def enable(self) -> None:
        '''
        Function to enable the motor for operation.
        '''
        self.enable_pin.value(0)
        self.enabled = True
        utime.sleep_ms(50)

    def disable(self) -> None:
        '''
        Function to disable the motor from operation.
        '''

        self.enable_pin.value(1)
        self.enabled = False

    def set_speed(self, speed) -> None:
        '''
        Function to set the motors speed.

        Parameters:
            speed: speed of motor in RPM.        
        '''

        # Calculating delay time between each step in microseconds (delay/step).
        # 1. Convert minute to microseconds.
        # 2. Divide by total number of steps per revolution.
        # 3. Divide by desired speed in steps per minute.
        delay = ((60*1e3*1e3) / self.steps_per_rev) / speed
        self.delay = round(delay)

    def get_speed(self) -> float:
        '''
        Function to calculate the speed of the motor in rpm.
        '''
        rpm = 1/(self.steps_per_rev * self.delay) * 60 * 1e3 * 1e3
        return round(rpm, 2)

    def set_direction(self, direction: int):
        '''
        Function to set the direcion of the motor
        '''
        if direction not in [CCW, CW]:
            raise ValueError(
                'Direction must be either "0 - Counter-Clockwise" or "1 - Clockwise" ')

        if direction == CCW:
            self.direction = CCW
            self.dir_pin.value(CCW)
        else:
            self.direction = CW
            self.dir_pin.value(CW)

    def old_move_steps(self, steps):
        '''
        Function to move motor a given number of steps.
        '''

        if self.enabled is False:
            raise ValueError("The stepper motor must be enabled to operate.")

        # Positive steps rotate counter-clockwise.
        # Negative steps rotate clockwise.
        if steps > 0:
            self.set_direction(CCW)
        elif steps < 0:
            self.set_direction(CW)

        steps_to_do = abs(steps)
        while steps_to_do > 0:
            steps_to_do -= 1
            self.step_pin.value(0)
            self.step_pin.value(1)
            utime.sleep_us(self.delay)

# ************************* TESTING *************************


def example1():

    stepper1 = Stepper(step_per_rev=200,
                       dir_pin=0,
                       step_pin=1,
                       enable_pin=2)
    stepper1.set_speed(100)
    stepper1.enable()

    for _ in range(2):
        stepper1.old_move_steps(200)
        utime.sleep(0.25)
        stepper1.old_move_steps(-200)
        utime.sleep(0.5)

    utime.sleep(0.5)
    stepper1.old_move_steps(200)
    stepper1.old_move_steps(-200)
    utime.sleep(0.5)

    stepper1.set_speed(800)
    stepper1.old_move_steps(2500)

    stepper1.disable()


if __name__ == '__main__':

    try:

        stepper1 = Stepper(step_per_rev=200,
                           dir_pin=0,
                           step_pin=1,
                           enable_pin=2)

        example1()

        stepper1.disable()
    except KeyboardInterrupt:
        stepper1.disable()
