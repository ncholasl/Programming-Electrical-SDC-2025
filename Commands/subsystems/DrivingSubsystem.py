import time
from gpiozero import Motor

def clamp(x, lo=-1.0, hi=1.0):
    return max(lo, min(hi, x))

def deadband(x, db=0.08):
    if abs(x) < db:
        return 0.0
    return (abs(x) - db) / (1.0 - db) * (1 if x > 0 else -1)

class Drivetrain:
    def __init__(self, left_motor: Motor, right_motor: Motor):
        self.left_motor = left_motor
        self.right_motor = right_motor

        # desired state 
        self.left_target = 0.0
        self.right_target = 0.0

        self.enabled = True
        self.last_command_time = time.monotonic()

        self.watchdog_timeout = 0.4  # seconds

    # === DRIVER INTERFACE ===
    def tank_drive(self, left, right):
        self.left_target = deadband(clamp(left))
        self.right_target = deadband(clamp(right))
        self.last_command_time = time.monotonic()

    def stop(self):
        self.left_target = 0.0
        self.right_target = 0.0

    # === PERIODIC LOOP ===
    def periodic(self):
        # watchdog
        if time.monotonic() - self.last_command_time > self.watchdog_timeout:
            self.stop()

        if not self.enabled:
            self.left_motor.stop()
            self.right_motor.stop()
            return

        self._apply_motor(self.left_motor, self.left_target)
        self._apply_motor(self.right_motor, self.right_target)

    # === HARDWARE LAYER ===
    @staticmethod
    def _apply_motor(motor: Motor, value: float):
        if value > 0:
            motor.forward(value)
        elif value < 0:
            motor.backward(-value)
        else:
            motor.stop()
