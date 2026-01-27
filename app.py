from flask import Flask, render_template, Response, request
import cv2
from hardware import RobotHardware # Using the class we built earlier!

app = Flask(__name__)
robot = RobotHardware()

# 1. Camera Stream Logic
def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 2. Control Logic
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    cmd = request.form.get('action')
    if cmd == 'forward': robot.drive_forward()
    elif cmd == 'stop': robot.stop()
    elif cmd == 'sort': robot.kick_sorting_arm()
    # Add your arm movements here
    return "OK", 200

if __name__ == '__main__':
    # '0.0.0.0' makes it accessible to your phone on the same network
    app.run(host='0.0.0.0', port=5000, threaded=True)
