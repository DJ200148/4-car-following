from flask import Flask, jsonify, request, render_template


def create_app(controller, index_page_path, template_folder='../templates', shared_state=None):
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

    @app.route('/stop', methods=['POST'])
    def stop():
        try:
            controller.stop()
            if shared_state is not None:
                shared_state['STOP'] = True  # Update the shared state
            return jsonify({'message': 'RC car and server shutting down'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app