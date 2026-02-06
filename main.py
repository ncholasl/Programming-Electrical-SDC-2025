from gpiozero import PWMLED
from gpiozero import LED
import time
from crsf_parser import CRSFParser, PacketValidationStatus
from serial import Serial

"""
LEFT_FORWARD_PIN = 16
LEFT_BACKWARD_PIN = 20
LEFT_ENABLE_PIN = 21
RIGHT_FORWARD_PIN = 19
RIGHT_BACKWARD_PIN = 26
RIGHT_ENABLE_PIN = 13
"""

# Pin definitions
LEFT_FORWARD_PIN = PWMLED(16)
LEFT_BACKWARD_PIN = PWMLED(20)
LEFT_ENABLE_PIN = LED(21)
RIGHT_FORWARD_PIN = PWMLED(19)
RIGHT_BACKWARD_PIN = PWMLED(26)
RIGHT_ENABLE_PIN = LED(13)

# Controller variables
channel_values = []
lower_threshold = 174
higher_threshold = 1811
deadzone_buffer = 100
center = (higher_threshold + lower_threshold) / 2


def frame_parser(frame, status):
    global channel_values
    if hasattr(frame, "payload") and hasattr(frame.payload, "channels"):
        channel_values = []
        for val in frame.payload.channels:
            channel_values.append(val)
        else:
            pass  
        channel_values.reverse()


def drivetrain_motor_control():
    left_control = channel_values[0]  # Channel 1 controls the left motor
    right_control = channel_values[1]  # Channel 2 controls the right motor

    # Calculate deadzone bounds
    dead_left_lower_bound = center - deadzone_buffer
    dead_left_upper_bound = center + deadzone_buffer

    
    # Start with left motor control
    if lower_threshold - deadzone_buffer < left_control < dead_left_lower_bound:
        # Upper bound past deadzone for motor to move backwards
        LEFT_FORWARD_PIN.off()
        LEFT_BACKWARD_PIN.on()
        LEFT_ENABLE_PIN.on()
        #left_pwm_value = max(0.0, min(1.0, (left_control - dead_left_lower_bound) / (dead_left_lower_bound - lower_threshold)))
        
        # Normalize left_control (lower_threshold to dead_left_lower_bound) to a PWM value (0.0 to 1.0)
        LEFT_BACKWARD_PIN.value  = max(0.0, min(1.0, 1 - (left_control - lower_threshold) / (dead_left_lower_bound - lower_threshold)))


    elif dead_left_upper_bound  < left_control < higher_threshold + deadzone_buffer:
        # Upper bound past deadzone for motor to move forward
        LEFT_BACKWARD_PIN.off()
        LEFT_FORWARD_PIN.on()
        LEFT_ENABLE_PIN.on()

        # Normalize left_control (dead_left_upper_bound to higher_threshold) to a PWM value (0.0 to 1.0)
        LEFT_FORWARD_PIN.value = max(0.0, min(1.0, (left_control - dead_left_upper_bound) / (higher_threshold - dead_left_upper_bound)))
    
    else:
        # Stick is in deadzone, stop motors
        LEFT_FORWARD_PIN.off()
        LEFT_BACKWARD_PIN.off()
        LEFT_ENABLE_PIN.off()
        LEFT_BACKWARD_PIN.value = 0
        LEFT_FORWARD_PIN.value = 0

    # Right motor control
    if lower_threshold - deadzone_buffer< right_control < dead_left_lower_bound:
        # Upper bound past deadzone for motor to move backwards
        RIGHT_FORWARD_PIN.off()
        RIGHT_BACKWARD_PIN.on()
        RIGHT_ENABLE_PIN.on()
        #left_pwm_value = max(0.0, min(1.0, (left_control - dead_left_lower_bound) / (dead_left_lower_bound - lower_threshold)))
        
        # Normalize right_control (lower_threshold to dead_left_lower_bound) to a PWM value (0.0 to 1.0)
        RIGHT_BACKWARD_PIN.value  = max(0.0, min(1.0, 1 - (right_control - lower_threshold) / (dead_left_lower_bound - lower_threshold)))

    elif dead_left_upper_bound < right_control < higher_threshold + deadzone_buffer:
        # Upper bound past deadzone for motor to move forward
        RIGHT_BACKWARD_PIN.off()
        RIGHT_FORWARD_PIN.on()
        RIGHT_ENABLE_PIN.on()

        # Normalize right_control (dead_left_upper_bound to higher_threshold) to a PWM value (0.0 to 1.0)
        RIGHT_FORWARD_PIN.value = max(0.0, min(1.0, (right_control - dead_left_upper_bound) / (higher_threshold - dead_left_upper_bound)))
    
    else:
        # Stick is in deadzone, stop motors
        RIGHT_FORWARD_PIN.off()
        RIGHT_BACKWARD_PIN.off()
        RIGHT_ENABLE_PIN.off()
        RIGHT_BACKWARD_PIN.value = 0
        RIGHT_FORWARD_PIN.value = 0



parser = CRSFParser(frame_parser)

# Open Serial for the reciever and start main loop
with Serial("/dev/ttyAMA0", 425000, timeout=2) as ser:
    # Create buffer to store reciever data
    buffer = bytearray()

    while True:
        # Pull data from reciever and parse
        data = ser.read(100)
        buffer.extend(data)
        parser.parse_stream(buffer)


        drivetrain_motor_control()
        print(f"Channel Values: {channel_values}")
        print(f"Left Motor - Forward: {LEFT_FORWARD_PIN.value:.2f}, Backward: {LEFT_BACKWARD_PIN.value:.2f}, Enable: {LEFT_ENABLE_PIN.is_active}")        
        print(f"Right Motor - Forward: {RIGHT_FORWARD_PIN.value:.2f}, Backward: {RIGHT_BACKWARD_PIN.value:.2f}, Enable: {RIGHT_ENABLE_PIN.is_active}")