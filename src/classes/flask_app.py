from flask import Flask, jsonify, request, render_template, Response
from classes.autonomous_rc_controller_avoid import AutonomousRCController
from classes.status_enum import Status
import time
# from classes.autonomous_rc_controller_interface import AutonomousRCControllerInterface


def create_app(controller: AutonomousRCController, index_page_path, template_folder='/templates', shared_state=None):
    app = Flask(__name__, template_folder=template_folder)
    
    # Flask endpoints
    @app.route('/')
    def index():
        return render_template(index_page_path)

    @app.route('/start', methods=['GET'])
    def start():
        # Check if the status is not ready
        if controller.get_status() != Status.READY:
            return jsonify({'error': f'The RC is not ready, current status: {controller.get_status()}'}), 409
        
        # Get the 'coords' query parameter as a comma-separated string (e.g., "x,y")
        coords_string = request.args.get('coords', '')
        
        try:
            # Attempt to split the string into parts and convert each to float (or int, as needed)
            coords = tuple(float(coord.strip()) for coord in coords_string.split(','))
            if len(coords) != 2:
                raise ValueError
            try:
                controller.start(coords)
                return jsonify({'message': f"RC car started with coordinates {coords}"}), 200
            except Exception as e:
                # Handle any errors from the controller method
                return jsonify({'error': str(e)}), 500
        except ValueError:
            # Handle the case where conversion fails
            return jsonify({'error': 'Invalid coordinates format. Please provide them in x,y format.'}), 400

    @app.route('/pause', methods=['GET'])
    def pause():
        # Check if the status is not running
        if controller.get_status() != Status.RUNNING:
            return jsonify({'error': f'The RC is not running, current status: {controller.get_status()}'}), 409
        
        try:
            controller.pause()
            return jsonify({'message': 'RC car paused'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/resume', methods=['GET'])
    def resume():
        # Check if the status is not paused
        if controller.get_status() != Status.PAUSED:
            return jsonify({'error': f'The RC is not paused, current status: {controller.get_status()}'}), 409
        
        try:
            controller.resume()
            return jsonify({'message': 'RC car resumed'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    @app.route('/reset', methods=['GET'])
    def reset():
        try:
            controller.reset()
            return jsonify({'message': 'RC car reset'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        try:
            controller.stop()
            if shared_state is not None:
                shared_state['STOP'] = True  # Update the shared state
            return jsonify({'message': 'RC car and server shutting down'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/status', methods=['GET'])
    def status():
        return jsonify({'message': f'RC car status: {controller.get_status()}'})
    
    def generate_camera_stream_color_image():
        while True:
            while controller.get_status() != Status.READY and controller.get_status() != Status.RUNNING and controller.get_status() != Status.PAUSED:
                pass
            frame = controller.depth_camera.get_jpeg_color_image_frame(True)
            if frame:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                # Handle error or no frame scenario
                time.sleep(0.1)  # Prevent tight loop if there's an error

    @app.route('/video_feed_color_image')
    def video_feed_color_image():
        """Route to stream video from the camera."""
        return Response(generate_camera_stream_color_image(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    def generate_camera_stream_depth_colormap():
        while True:
            while controller.get_status() != Status.READY and controller.get_status() != Status.RUNNING and controller.get_status() != Status.PAUSED:
                pass
            frame = controller.depth_camera.get_jpeg_depth_colormap_frame(True)
            if frame:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                # Handle error or no frame scenario
                time.sleep(0.1)  # Prevent tight loop if there's an error

    @app.route('/video_feed_depth_colormap')
    def video_feed_depth_colormap():
        """Route to stream video from the camera."""
        return Response(generate_camera_stream_depth_colormap(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    return app