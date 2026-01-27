import os
import sys
import time
import select
import termios
import tty

from gpiozero import Motor, Device
from gpiozero.pins.mock import MockFactory
from gpiozero.exc import PinPWMUnsupported

# If this file is executed directly (python Commands/driving_teleop.py),
# Python sets `__package__` to None and `sys.path[0]` becomes the
# `Commands/` directory. That prevents `from Commands...` imports from
# resolving. Ensure the project root is on `sys.path` so package imports
# work when running the script by path.
if __package__ is None:
    import pathlib
    import sys

    project_root = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root))

from Commands.constants import INPUT_TIMEOUT, LOOP_HZ
from Commands.subsystems.DrivingSubsystem import Drivetrain


if os.uname().sysname != "Linux":
    Device.pin_factory = MockFactory()


LEFT_FORWARD_PIN = 16
LEFT_BACKWARD_PIN = 20
LEFT_ENABLE_PIN = 21
RIGHT_FORWARD_PIN = 19
RIGHT_BACKWARD_PIN = 26
RIGHT_ENABLE_PIN = 13

DRIVE_SPEED = 0.6


def _read_key(timeout=0.0):
    if select.select([sys.stdin], [], [], timeout)[0]:
        return sys.stdin.read(1)
    return None


def main():
    def _make_motor(forward, backward, enable):
        try:
            return Motor(forward=forward, backward=backward, enable=enable)
        except PinPWMUnsupported:
            # Mock pin factory doesn't support PWM on the enable pin.
            # Fall back to creating the Motor without an enable pin so
            # the code can run in mock/testing environments.
            print("Warning: PWM not supported on enable pin; creating Motor without enable")
            return Motor(forward=forward, backward=backward)

    left_motor = _make_motor(LEFT_FORWARD_PIN, LEFT_BACKWARD_PIN, LEFT_ENABLE_PIN)
    right_motor = _make_motor(RIGHT_FORWARD_PIN, RIGHT_BACKWARD_PIN, RIGHT_ENABLE_PIN)
    drivetrain = Drivetrain(left_motor, right_motor)

    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        last_input_time = 0.0
        left_cmd = 0.0
        right_cmd = 0.0

        print("WASD drive | space=stop | q=quit")
        while True:
            key = _read_key(timeout=1.0 / LOOP_HZ)
            now = time.monotonic()

            if key:
                last_input_time = now
                if key in ("w", "W"):
                    left_cmd = DRIVE_SPEED
                    right_cmd = DRIVE_SPEED
                elif key in ("s", "S"):
                    left_cmd = -DRIVE_SPEED
                    right_cmd = -DRIVE_SPEED
                elif key in ("a", "A"):
                    left_cmd = -DRIVE_SPEED
                    right_cmd = DRIVE_SPEED
                elif key in ("d", "D"):
                    left_cmd = DRIVE_SPEED
                    right_cmd = -DRIVE_SPEED
                elif key == " ":
                    left_cmd = 0.0
                    right_cmd = 0.0
                elif key in ("q", "Q"):
                    break

            if now - last_input_time > INPUT_TIMEOUT:
                drivetrain.tank_drive(0.0, 0.0)
            else:
                drivetrain.tank_drive(left_cmd, right_cmd)

            drivetrain.periodic()
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        drivetrain.tank_drive(0.0, 0.0)
        drivetrain.periodic()


if __name__ == "__main__":
    main()
