import numpy as np
import cv2

class RobotVision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0) # 0 is the Macbook's built-in camera
        self.lower_color = np.array([30, 150, 50])  # Lower bound for green color in HSV
        self.upper_color = np.array([85, 255, 255]) # Upper bound for green color in HSV

    def get_target_coordinates():
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, self.lower_color, self.upper_color)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest)
            if M["m00"] > 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                return (cX, cY)
        return None
    
    def close(self):
        self.cap.release()