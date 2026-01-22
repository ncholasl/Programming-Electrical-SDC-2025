import time
from vision import RobotVision
from hardware import RobotHardware

vision = RobotVision()
robot = RobotHardware()

# The sorting "queue" (timestamps of when waste was seen)
waste_on_belt = []
BELT_TRAVEL_TIME = 2.5 # Seconds from camera to kicker

print("Robot System Initialized (MOCK MODE)")

try:
    while True:
        # 1. Look for waste
        coords = vision.get_target_coords()
        if coords:
            print(f"Waste seen at {coords}! Adding to queue.")
            waste_on_belt.append(time.time() + BELT_TRAVEL_TIME)
            # Give some "cool down" so we don't double-detect
            time.sleep(0.5)

        # 2. Check if any waste has reached the kicker
        current_time = time.time()
        for kick_time in waste_on_belt[:]:
            if current_time >= kick_time:
                print(">>> KICKING WASTE INTO HOPPER!")
                robot.kicker.min()
                time.sleep(0.3)
                robot.kicker.max()
                waste_on_belt.remove(kick_time)

        # 3. Keep the belt moving
        robot.conveyor.forward(0.5) 
        
        time.sleep(0.1)

except KeyboardInterrupt:
    robot.stop()
    vision.close()
