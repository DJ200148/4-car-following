import pyrealsense2 as rs
import numpy as np
import cv2

# Initialize depth camera settings
DEPTH_WIDTH = 640
DEPTH_HEIGHT = 480
FPS = 30

# Video writer initialization
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec and create VideoWriter object
# Make sure the 'isColor' flag is True for colored images and False for grayscale images
out = cv2.VideoWriter('output.avi', fourcc, FPS, (DEPTH_WIDTH, DEPTH_HEIGHT), True)

# Start the depth camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, DEPTH_WIDTH, DEPTH_HEIGHT, rs.format.z16, FPS)
pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())

        # Convert the depth image to a visual format that is suitable for human viewing
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Recalculate the size of each grid and display depth values
        grid_rows, grid_cols = 4, 4
        grid_height, grid_width = DEPTH_HEIGHT // grid_rows, DEPTH_WIDTH // grid_cols
        min_depths = np.zeros((grid_rows, grid_cols))

        for i in range(grid_rows):
            for j in range(grid_cols):
                grid = depth_image[i*grid_height:(i+1)*grid_height, j*grid_width:(j+1)*grid_width]
                grid = grid[grid > 0]  # Ignore depth value 0
                if grid.size > 0:
                    min_depth = grid.min()
                else:
                    min_depth = np.nan  # Assign NaN if no valid depth values
                min_depths[i, j] = min_depth
                cv2.putText(depth_colormap, f"{min_depth:.2f}", (j*grid_width+5, i*grid_height+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

        # Draw grid lines
        for i in range(1, grid_rows):
            cv2.line(depth_colormap, (0, i*grid_height), (DEPTH_WIDTH, i*grid_height), (255, 255, 255), 1, lineType=cv2.LINE_AA)
        for j in range(1, grid_cols):
            cv2.line(depth_colormap, (j*grid_width, 0), (j*grid_width, DEPTH_HEIGHT), (255, 255, 255), 1, lineType=cv2.LINE_AA)

        # Save the frame into the file 'output.avi'
        out.write(depth_colormap)

        cv2.imshow('Depth Image with Grids', depth_colormap)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    pipeline.stop()
    out.release()  # Release the VideoWriter object
    cv2.destroyAllWindows()
