# Here we will combine all the pipelines and run them in a sequence

# Imports
from classes.autonomous_rc_controller import AutonomousRCController
from flask import Flask, jsonify, request, render_template



#### NOTES ####
# Real time is 24 fps

## Pipeline Steps
# Init all nessary classes and helpers
# Check the GPS locations of where you start and end
# Find the shortest path between the two points that is drivable
# if no path notfiy the user

# Loop
# Get GPS location
# ensure that the rc is on the shortest path, if not then correct it
# Gather input data from the camera (image + depth)
# Detect objects in the input data
# determine if the rc needs to avoid an object via the detection and distances
# make any nessary adjustments to the rc,
    # like slowing down, stopping, turning or reversing
### END NOTES ###

# Constants
STOP = False
INDEX_HTML_PATH = 'index.html'

app = Flask(__name__, template_folder='../templates')

# Initialize the RC Controller
controller = AutonomousRCController(5) # this takes at least 60 seconds to initialize
print("RC Controller Initialized.")

@app.route('/')
def index():
    return render_template(INDEX_HTML_PATH)

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

@app.route('/shutdown', methods=['POST'])
def shutdown():
    try:
        controller.shutdown()
        global STOP
        STOP = True
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return jsonify({'message': 'RC car and server shutting down'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)