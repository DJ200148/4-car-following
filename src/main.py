# Here we will combine all the pipelines and run them in a sequence

# Imports
import os, signal, time, threading
from classes.autonomous_rc_controller import AutonomousRCController
from classes.flask_app import create_app


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

# Define a shared state object
shared_state = {'STOP': False}

# Controller calibrations
TEST_MODE = False
LOW_THRESHOLD = 400
HIGH_THRESHOLD = 700
OFFSET = 7

# Initialize the RC Controller
controller = AutonomousRCController(test_mode=TEST_MODE, low_threshold=LOW_THRESHOLD, high_threshold=HIGH_THRESHOLD, offset=OFFSET) # this takes at least 60 seconds to initialize
print("RC Controller created, but will need to still wait for init to complete.")

# Initialize the Flask app
INDEX_HTML_PATH = 'index.html'
app = create_app(controller, INDEX_HTML_PATH, template_folder='../../templates', shared_state=shared_state)

def run_flask():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
   

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    while not shared_state['STOP']:
        pass

    # Stop the Flask app
    time.sleep(1)
    os.kill(os.getpid(), signal.SIGTERM)