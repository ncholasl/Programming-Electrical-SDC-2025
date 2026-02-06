from gpiozero import PWMLED
from gpiozero import LED
import time
from crsf_parser import CRSFParser, PacketValidationStatus
from serial import Serial


values = []
lower_threshold = 0
higher_threshold = 2000
deadzone_buffer = 100
center = (higher_threshold + lower_threshold) / 2



def drivetrain_motor_control():
    left_control = 0

    dead_left_lower_bound = center - deadzone_buffer
    dead_left_upper_bound = center + deadzone_buffer

    left_pwm_value = 0.0

    # Lower ramp (1 → 0)
    if lower_threshold <= left_control <= dead_left_lower_bound:
        LEFT_FORWARD_PIN.off()
        LEFT_BACKWARD_PIN.on()
        raw = (
            (dead_left_lower_bound - left_control)
            / (dead_left_lower_bound - lower_threshold)
        )
        left_pwm_value = max(0.0, min(1.0, raw))

    # Upper ramp (0 → 1)
    elif dead_left_upper_bound <= left_control <= higher_threshold:
        LEFT_FORWARD_PIN.on()
        LEFT_BACKWARD_PIN.off()
        raw = (
            (left_control - dead_left_upper_bound)
            / (higher_threshold - dead_left_upper_bound)
        )
        left_pwm_value = max(0.0, min(1.0, raw))

    else:
        left_pwm_value = 0.0 

    print(f"Left PWM Value: {left_pwm_value:.2f}")


drivetrain_motor_control()