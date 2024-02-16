import pyrealsense2 as rs
import numpy as np

# Initialize depth camera settings
DEPTH_WIDTH = 640
DEPTH_HEIGHT = 480
FPS = 30

# Set the number of grids
grid_rows = 4  # Number of rows in the grid
grid_cols = 4  # Number of columns in the grid

# Start the depth camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, DEPTH_WIDTH, DEPTH_HEIGHT, rs.format.z16, FPS)
pipeline.start(config)

try:
    # Continuously capture frames from the depth camera
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue  # If no depth frame is captured, try again

        # Convert the depth frame to a NumPy array
        depth_image = np.asanyarray(depth_frame.get_data())

        # Recalculate the size of each grid based on the new grid numbers
        grid_height, grid_width = DEPTH_HEIGHT // grid_rows, DEPTH_WIDTH // grid_cols

        # Reinitialize the array to store the minimum depth values
        min_depths = np.zeros((grid_rows, grid_cols))

        # Update loop to process the new number of grids
        for i in range(grid_rows):
            for j in range(grid_cols):
                grid = depth_image[i*grid_height:(i+1)*grid_height, j*grid_width:(j+1)*grid_width]
                grid = grid[grid > 0]  # Ignore cases where depth value is 0
                if grid.size > 0:
                    min_depths[i, j] = grid.min()
                else:
                    min_depths[i, j] = np.nan  # Assign NaN if there are no valid depth values in the grid

        # Print the minimum depth values for each grid
        print("Minimum depth value in meters for each grid:\n", min_depths * depth_frame.get_units())

finally:
    pipeline.stop()
