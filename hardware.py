from gpiozero import Motor, Servo, OutputDevice
from gpiozero.pins.mock import MockFactory
import os

# Ensure mock factory is used if on Mac
if os.uname().sysname != 'Linux':
    from gpiozero import Device
    Device.pin_factory = MockFactory()

class RobotHardware:
    def __init__(self):
        # Drive Train (4 Motors)
        self.left_front = Motor(forward=17, backward=18)
        self.right_front = Motor(forward=22, backward=23)
        
        # Conveyor & Sorting
        self.conveyor = Motor(forward=24, backward=25)
        self.kicker = Servo(12) # Servo for the "Kick Arm"

        # 5-DOF Arm (Mocking pins)
        self.arm_base = Servo(5)
        self.arm_shoulder = Servo(6)
        self.arm_elbow = Servo(13)
        self.arm_wrist = Servo(19)
        self.arm_claw = Servo(26)

    def drive_forward(self):
        print("MOCK: Driving Forward")
        self.left_front.forward()
        self.right_front.forward()

    def stop(self):
        self.left_front.stop()
        self.right_front.stop()
        self.conveyor.stop()