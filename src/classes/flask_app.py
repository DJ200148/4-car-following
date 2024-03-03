from flask import Flask, jsonify, request, render_template, Response
from classes.autonomous_rc_controller import AutonomousRCController
import time


def create_app(controller: AutonomousRCController, index_page_path, template_folder='/templates', shared_state=None):
    app = Flask(__name__, template_folder=template_folder)
    
    # Flask endpoints
    @app.route('/')
    def index():
        return render_template(index_page_path)

    @app.route('/start', methods=['GET'])
    def start():
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
        try:
            controller.pause()
            return jsonify({'message': 'RC car paused'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/resume', methods=['GET'])
    def resume():
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
        return jsonify({'message': f'RC car status: {controller.status}'})
    
    def generate_camera_stream():
        while True:
            frame = controller.depth_camera.get_jpeg_frame()
            if frame:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                # Handle error or no frame scenario
                time.sleep(0.1)  # Prevent tight loop if there's an error

    @app.route('/video_feed')
    def video_feed():
        """Route to stream video from the camera."""
        return Response(generate_camera_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return app