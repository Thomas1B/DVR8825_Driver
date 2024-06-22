'''
Basic Stepper Class for Pi Pico using the DVR8825 Motor Driver.
'''

from machine import Pin  # type: ignore
import utime  # type: ignore

# Default direction values for the DVR8825
dvr_CCW = 0  # Counter-Clockwise direction
dvr_CW = 1  # Clockwise direction.


# Global constants for ease
HIGH = 1  # high value for Pins.
LOW = 0  # low value for Pins.


class Stepper:

    def __init__(self, step_pin: int, dir_pin: int, enable_pin: int, step_mode=1, **kwargs) -> None:
        """
        Initializes the stepper motor controller instance.

        Parameters:
            step_pin (int): Pin number for step signal.
            dir_pin (int): Pin number for direction signal.
            enable_pin (int): Pin number for enable signal.
            step_mode (int): Optional parameter specifying the step mode.
                        Default is 1 (full step).
                        Supported values:
                        - 1: Full step
                        - 2: Half step
                        - 4: Quarter step
                        - 8: 1/8 step
                        - 16: 1/16 step
                        - 32: 1/32 step

            **kwargs:
                mode_pins (tuple[int | none]): Tuple containing 3 pin numbers (m0, m1, m2) for setting step mode.
                                    These pins can alternatively be hardwired to 3.3V to free up more GPIO pins on the Pico.
        """

        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.enable_pin = Pin(enable_pin, Pin.OUT)

        # Class constants
        self.CCW = dvr_CW  # Counter-Clockwise direction
        self.CW = dvr_CCW  # Clockwise direction.

        if 'mode_pins' in kwargs:
            # Checking if 'mode_pins' is in **kwargs, if so initialize pins
            m0, m1, m2 = kwargs['mode_pins']
            self._m0_pin = Pin(m0, Pin.OUT) if m0 is not None else None
            self._m1_pin = Pin(m1, Pin.OUT) if m1 is not None else None
            self._m2_pin = Pin(m2, Pin.OUT) if m2 is not None else None
            self.set_step_mode(step_mode)
        else:
            self.step_mode = step_mode

        self.target_position = 0  # target position in steps
        self.position = 0  # position in steps
        self.direction = self.CCW

    def set_step_mode(self, step_mode=1) -> None:
        '''
        Function to set the step mode of the motor:

        Parameters:
            step_mode:
                    Default is 1 (full step).
                    Supported values:
                    - 1: Full step
                    - 2: Half step
                    - 4: Quarter step
                    - 8: 1/8 step
                    - 16: 1/16 step
                    - 32: 1/32 step
        '''
        step_modes = {
            1: (0, 0, 0),    # Full step
            2: (1, 0, 0),    # Half step
            4: (0, 1, 0),    # Quarter step
            8: (1, 1, 0),    # 1/8 step
            16: (0, 0, 1),   # 1/16 step
            32: (1, 0, 1),   # 1/32 step
        }

        m_pins = [self._m0_pin, self._m1_pin, self._m2_pin]

        if step_mode in step_modes:
            self.step_mode = step_mode
            for pin, val in zip(m_pins, step_modes[step_mode]):
                if pin:
                    pin.value(val)

    def enable(self) -> None:
        '''
        Function to enable the motor for operation.
        '''
        self.enabled = True
        if self.enable_pin:
            self.enable_pin.value(LOW)

    def disable(self) -> None:
        '''
        Function to disable the motor from operation.
        '''

        self.enabled = False
        if self.enable_pin:
            self.enable_pin.value(HIGH)

    def set_speed(self, speed: float) -> None:
        '''
        Set the speed of the stepper motor.

        The speed is defined as the number of steps the motor takes per second.
        Only the absolute value of the speed is used to calculate the delay between steps.

        Parameters:
            speed (float): The desired speed of the motor in steps per second.
                    The speed cannot be zero as it would lead to an infinite delay.

        Returns:
            None
        '''
        self.delay = 1 / abs(speed)  # delay in seconds

    def _flip_ccw_cw(self) -> None:
        '''
        Function to flip the values of counter-clockwise and clockwise.
            - Useful for running two motors in oppsite direction running same axis.

        CCW -> CW
        CW -> CCW

        '''
        self.CCW = not self.CCW
        self.CW = not self.CW

    def set_direction(self, direction: 0 | 1) -> None:
        '''
        Set the direction of the stepper motor.

        Parameters:
            direction (1 | 0): The desired direction of the motor rotation.

        Returns:
            None
        '''
        self.dir_pin.value(direction)
        self.direction = direction

    def set_target_pos(self, target_pos: int) -> None:
        '''
        Function to set the target position of the motor in absolute positioning.

        Parameters:
            target_pos: target position in steps.

        Returns:
            None
        '''
        self.target_position = target_pos

    def steps_to_target(self) -> float:
        '''
        Function to get the number of steps to the target position
        '''

        distance = self.target_position - self.position
        return distance

    def one_step(self) -> None:
        '''
        Function to take one step.
        '''
        self.step_pin.value(1)
        utime.sleep(self.delay)
        self.step_pin.value(0)

    def move_to_abs(self, target_pos: int) -> None:
        '''
        Move the stepper motor to the target position in absolute steps.

        Parameters:
            target_pos (int): The desired target position in steps, in absolute position.

        Returns:
            None
        '''
        self.set_target_pos(target_pos)
        self.set_direction(self.CW if target_pos > self.position else self.CCW)

        step_increment = 1 if self.direction == self.CW else -1
        while self.steps_to_target() != 0:
            self.one_step()
            self.position += step_increment / self.step_mode  # compensate for microstepping


# **************************** Examples ****************************
if __name__ == '__main__':
    # Define the pins
    stepper = Stepper(step_pin=1, dir_pin=0, enable_pin=2,
                      mode_pins=(3, 4, 5))
    stepper.set_step_mode(2)
    stepper.set_speed(500)
    stepper.enable()

    steps = 200

    limit_swt = Pin(14, Pin.IN)

    try:
        print(f'Before: {stepper.position}')
        stepper.move_to_abs(2000)
        print(f'after: {stepper.position}')

        stepper.disable()

    except KeyboardInterrupt:
        stepper.disable()
