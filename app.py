from flask import Flask, render_template, request, Response
from hardware import RobotArm
import cv2

app = Flask(__name__)
arm = RobotArm()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    joint = request.form.get('joint')
    direction = request.form.get('dir') # 'up' or 'down'
    step = 10 if direction == 'up' else -10
    
    arm.move_joint(joint, step)
    return "OK", 200

# (Include your gen_frames() and video_feed route from the previous step here)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
