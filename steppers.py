
from machine import Pin  # type: ignore
import utime


class Stepper:

    CCW = 0  # Counter-Clockwise.
    CW = 1  # Clockwise.

    HIGH = 1
    LOW = 0

    def __init__(self, step_pin, dir_pin, enable_pin):
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.enable_pin = Pin(enable_pin, Pin.OUT)

        self.position = 0

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

    def set_speed(self, speed):
        self.delay = 1 / abs(speed)  # delay in seconds

    def set_direction(self, direction):
        self.dir_pin.value(direction)

    def move_to(self, target_pos):
        self.set_direction(1 if target_pos > self.position else 0)
        while self.position != target_pos:
            self.step_pin.value(1)
            utime.sleep(self.delay)
            self.step_pin.value(0)
            self.position += 1 if target_pos > self.position else -1


if __name__ == '__main__':
    print("Starting")

    steps = 2000

    # Define the pins
    dir_pin = 6   # GPIO number where dir pin is connected
    step_pin = 7  # GPIO number where step pin is connected
    enable_pin = 8  # GPIO number where step pin is connected
    stepper = Stepper(step_pin, dir_pin, enable_pin)

    limit_swt = Pin(14, Pin.IN)

    try:

        stepper.set_speed(500)
        stepper.enable()

        # stepper.set_direction(Stepper.CCW)
        stepper.move_to(steps)

        utime.sleep(2)
        # stepper.move_to(steps+10)
        # stepper.move_to(0)

        stepper.disable()
        print('Done!')

    except KeyboardInterrupt:
        stepper.disable()
