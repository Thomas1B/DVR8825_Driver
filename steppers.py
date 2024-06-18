'''
Micropython module for the DVR8825 Stepper motor drive to used with the Pi Pico.

If you are concerned about real-time performance, it is best to use an Arduino.

'''


import utime
from machine import Pin  # type: ignore


# ************** Functions *************


def check_limit_switches(pins=[Pin]) -> bool:
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
        results = [True if pin.value() == 1 else False for pin in pins]
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


class Stepper:
    '''
    Class for stepper motor control using a DVR8825 Stepper Driver.

    Parameters:
        name: reference name to help debugging
        dir_pin: pin number used for direction pin.
        step_pin: pin numbser used for step pin.
        enable_pin: pin number used for the enable pin.
        step_mode (default 1): microstep modes, 1 - full, 2 - half, 4, 8, 16, 32.
    '''

    CCW = 0  # Counter-Clockwise.
    CW = 1  # Clockwise.

    HIGH = 1
    LOW = 0

    def __init__(self,
                 name: str,
                 dir_pin: int,  # direction pin #.
                 step_pin: int,  # step pin #.
                 enable_pin=None,  # enable pin #.
                 ) -> None:

        self.__name = name
        self.__direction = None

        # Pin objects for direction, step and enable
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.enable_pin = Pin(enable_pin, Pin.OUT) if enable_pin else None

        self.enabled = False  # operating state of motor
        self.disable()

        self.__max_speed_interval = 0  # microseconds/step

    def enable(self) -> None:
        '''
        Function to enable the motor for operation.
        '''
        self.enabled = True
        if self.enable_pin:
            self.enable_pin.value(Stepper.LOW)

    def disable(self) -> None:
        '''
        Function to disable the motor from operation.
        '''

        self.enabled = False
        if self.enable_pin:
            self.enable_pin.value(Stepper.HIGH)

    def set_direction(self, dir: int):
        '''
        Function to set the direcion of the motor.

        Parameters:
            dir: direction motor spins, 0 - CCW, 1 - CW.
        '''
        if dir not in [self.CCW, self.CW]:
            raise ValueError(
                f'Invalid direction: "{dir}". Direction must be either "0" or CCW or "1" for CW.')

        if dir == self.CCW:
            self.__direction = self.CCW
            self.dir_pin.value(self.CCW)
        else:
            self.__direction = self.CW
            self.dir_pin.value(self.CW)

    def set_max_speed(self, steps_per_sec: float) -> None:
        '''
        Function to set the motor's max speed in steps/second.

        Parameters:
            steps_per_sec: speed of motor in steps/second.
        '''
        steps_per_sec = abs(steps_per_sec)

        if steps_per_sec == 0:  # speed is 0.
            self.__max_speed_interval = 0

        else:
            # Calculating delay time between each step in microseconds (delay/step).
            # 1e6 microseconds in 1 second.
            delay = (1/steps_per_sec) * 1e6
            self.__max_speed_interval = round(delay)  # microseconds/step

    def one_step(self) -> None:
        '''
        Function to take one step.

        Direction needs to be set before see "set_direction()"

        Parameters:
            None

        Returns:
            None
        '''

        if self.enabled is False:
            text = f'Motor "{self.__name}" is disabled. Enable it before operating.'
            raise ValueError(text)

        if self.__direction is None:
            raise ValueError(
                f'Direction for motor "{self.__name}" needs to be set before operating.')

        self.step_pin.value(0)
        self.step_pin.value(1)

    def stop(self):
        '''
        Function to stop the motor instantly
        '''
        self.step_pin.low()

    def move_steps(self, steps: int, condition_func=None, condition_params=None) -> None:
        '''
        Function to move motor a certain number of steps.
        Direction needs to be set before see "set_direction()"

        Parameters:
            steps: number of steps to take.
            condition_func: function to test some condition to stop motors.
            condition_params: parameters to be passed to the condition function.

        Returns: None
        '''

        for _ in range(abs(steps)):
            if condition_func and condition_func(condition_params):
                break

            self.one_step()
            utime.sleep_us(self.__max_speed_interval)

        self.stop()


# ************************* Example *************************
if __name__ == '__main__':
    print("Starting Example\n")

    limit_swt = Pin(14, Pin.IN)
    led = Pin('LED', Pin.OUT)

    try:

        steps = 200000

        stepper1 = Stepper(name='A',
                           dir_pin=6,
                           step_pin=7,
                           enable_pin=8,
                           )

        stepper1.set_max_speed(300)
        stepper1.enable()
        led.on()

        stepper1.set_direction(Stepper.CW)
        stepper1.move_steps(steps, check_limit_switches,
                            condition_params=[limit_swt])

        stepper1.disable()
        led.off()
        print('Done!')

    except KeyboardInterrupt:
        stepper1.disable()
        led.off()
