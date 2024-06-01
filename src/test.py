# Imports
import os
import signal
import time
import threading
from flask import Flask, jsonify, request, render_template, Response
import cv2
import torch
from classes.depth_camera import DepthCamera
from classes.yolo_model import YoloModel
from threading import Event, Lock

# Define a shared state object
shared_state = {'STOP': False}

# Initialize the Flask app
app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    try:
        shared_state['STOP'] = True
        return jsonify({'message': 'Server shutting down'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/video_feed_color_image', methods=['GET'])
def video_feed_color_image():
    # image = get_latest_detect_image()
    # if image:
    return Response(get_latest_detect_image(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # else:
    #     return jsonify({'error': 'No image available'}), 404

def run_flask():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

# Function to handle object detection
def detect_objects(cam, model):
    global detect_buf
    while not shared_state['STOP']:
        try:
            image, depth, depth_colormap = cam.get_image_data()
            
            if image.shape[2] == 1:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
            else:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            image = cv2.resize(image, (640, 640))
            
            # Convert the image to a tensor and normalize
            image_tensor = torch.tensor(image).float().permute(2, 0, 1).unsqueeze(0) / 255.0
            
            # Perform detection
            results = model.detect(image_tensor)
            
            # Draw detections
            image_with_detections = model.draw_detections(image, results)
            
            with detect_lock:
                detect_buf = image_with_detections

        except Exception as ex:
            print(ex)
            pass
        time.sleep(0.1)  # Adding a small sleep to prevent tight loop

# Function to get the latest detected image
def get_latest_detect_image():
    global detect_buf
    with detect_lock:
        image = detect_buf
        if image is None:
            return None
    ret, jpeg_frame = cv2.imencode('.jpg', image)
    if not ret:
        return None
    return jpeg_frame.tobytes()

if __name__ == "__main__":
    # Initialize camera and model
    cam = DepthCamera()
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = YoloModel('../weights/yolov8n.pt', device=device)
    detect_buf = None
    detect_lock = Lock()
    
    print("Init done")
    
    # Create and start the detection thread
    detection_thread = threading.Thread(target=detect_objects, args=(cam, model))
    detection_thread.start()

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Main loop to check for the stop condition
    try:
        while not shared_state['STOP']:
            time.sleep(0.1)
    except KeyboardInterrupt:
        shared_state['STOP'] = True

    # Stop the Flask app and detection thread
    detection_thread.join()
    flask_thread.join()
    cam.stop()
    os.kill(os.getpid(), signal.SIGTERM)
