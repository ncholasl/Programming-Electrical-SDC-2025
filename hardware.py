from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory # Better for smooth servo movement

class RobotArm:
    def __init__(self):
        # Define pins for your 5-DOF (Adjust these to your actual wiring!)
        self.base = AngularServo(17, min_angle=-90, max_angle=90)
        self.shoulder = AngularServo(27, min_angle=-90, max_angle=90)
        self.elbow = AngularServo(22, min_angle=-90, max_angle=90)
        self.wrist = AngularServo(23, min_angle=-90, max_angle=90)
        self.claw = AngularServo(24, min_angle=-90, max_angle=90)
        
        # Starting positions
        self.angles = {"base": 0, "shoulder": 0, "elbow": 0, "wrist": 0, "claw": 0}

    def move_joint(self, joint_name, step):
        # Calculate new angle
        new_angle = self.angles[joint_name] + step
        
        # Constraint check (Safety first for the presentation!)
        if -90 <= new_angle <= 90:
            self.angles[joint_name] = new_angle
            joint = getattr(self, joint_name)
            joint.angle = new_angle
            print(f"Moving {joint_name} to {new_angle}")
