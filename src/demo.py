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
from classes.status_enum import Status
from threading import Lock

# GLOBALS
detect_buf = None
detect_lock = Lock()
model = None
cam = None
# Define a shared state object
shared_state = Status.STOPPED

# Initialize the Flask app
app = Flask(__name__, template_folder='../templates')

# Get the home page
@app.route('/')
def index():
    return render_template('index.html')

# Get the status of the RC car
@app.route('/status', methods=['GET'])
def status():
    global shared_state
    return jsonify({'message': f'RC car status: {shared_state}'})

# Shutdown the server
@app.route('/shutdown', methods=['POST'])
def shutdown():
    global shared_state
    try:
        shared_state = Status.STOPPED
        return jsonify({'message': 'Server shutting down'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Reset the server
@app.route('/reset', methods=['GET'])
def reset():
    global shared_state
    try:
        reset_operations()
        shared_state = Status.READY
        return jsonify({'message': 'RC car reset'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def reset_operations():
    # Reset the camera
    global cam
    cam.stop()
    cam = DepthCamera()
    
    # Reset the model
    global model
    model = make_model()
    
# Start the server
@app.route('/start', methods=['GET'])
def start():
    global shared_state
    try:
        if shared_state != Status.READY:
            return jsonify({'error': 'RC car not ready, please check status.'}), 409
        shared_state = Status.RUNNING
        return jsonify({'message': 'RC car started'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Pause the server
@app.route('/pause', methods=['GET'])
def pause():
    global shared_state
    try:
        if shared_state != Status.RUNNING:
            return jsonify({'error': 'RC car not running, cannot pause.'}), 409
        shared_state = Status.PAUSED
        return jsonify({'message': 'RC car paused'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Resume the server
@app.route('/resume', methods=['GET'])
def resume():
    global shared_state
    try:
        if shared_state != Status.PAUSED:
            return jsonify({'error': 'RC car not paused, cannot resume.'}), 409
        shared_state = Status.RUNNING
        return jsonify({'message': 'RC car resumed'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

    
# Return a feed of the latest depth colormap image
@app.route('/video_feed_depth_colormap', methods=['GET'])
def video_feed_depth_colormap():
    return Response(generate_camera_stream_depth_colormap(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to generate a stream of depth colormap images     
def generate_camera_stream_depth_colormap():
    while True:
        frame = cam.get_jpeg_depth_colormap_frame(lines=True)
        if frame:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            time.sleep(0.1)
            
# Return a feed of the latest color image
@app.route('/video_feed_color_image', methods=['GET'])
def video_feed_color_image():
    return Response(generate_camera_stream_color_image(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to generate a stream of color images
def generate_camera_stream_color_image():
    while True:
        frame = cam.get_jpeg_color_image_frame()
        if frame:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            time.sleep(0.1)

# Return a feed of the latest detection image
@app.route('/video_feed_detection', methods=['GET'])
def video_feed_detection():
    return Response(generate_camera_stream_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_camera_stream_detection():
    while True:
        frame = get_latest_detect_image()
        if frame:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            time.sleep(0.1)
            
# Function to get the latest detected image
def get_latest_detect_image():
    global detect_buf
    global detect_lock
    
    with detect_lock:
        image = detect_buf
        if image is None:
            return None
    ret, jpeg_frame = cv2.imencode('.jpg', image)
    if not ret:
        return None
    return jpeg_frame.tobytes()


# Helper functions
def run_flask():
    print("Running Flask app")
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

def make_model():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = YoloModel('../weights/yolov8n.pt', device=device)
    return model

# Function to handle object detection
def detect_objects():
    global detect_buf
    global detect_lock
    global shared_state
    global model
    global cam
    
    print("Detection thread started")
    while shared_state != Status.STOPPED:
        while shared_state != Status.RUNNING:
            if shared_state == Status.STOPPED:
                break
            time.sleep(0.1)
        try:
            image, depth, depth_colormap = cam.get_image_data()
            
            if image.shape[2] == 1:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
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



def main():
    global shared_state
    global model
    global cam
    
    # Initialize camera and model
    cam = DepthCamera()
    model = make_model()
    
    # Set state ready
    shared_state = Status.READY
    
    # Create and start the detection thread
    detection_thread = threading.Thread(target=detect_objects)
    detection_thread.start()

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    print("Ready")
    
    # Main loop to check for the stop condition
    try:
        while shared_state != Status.STOPPED:
            time.sleep(0.1)
    except KeyboardInterrupt:
        shared_state = Status.STOPPED

    # Stop the Flask app and detection thread
    print("Joining model")
    detection_thread.join()
    print("Stopping camera")
    cam.stop()
    
    print("Shutting down main...")
    time.sleep(1)
    os.kill(os.getpid(), signal.SIGTERM)


# Run the main function
main()