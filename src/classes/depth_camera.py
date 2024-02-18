import pyrealsense2 as rs
import numpy as np
import cv2

class DepthCamera:
    def __init__(self, depth_width=640, depth_height=480, depth_fps=30, color_width=640, color_height=480, color_fps=30):
        # Initialize camera pipeline
        self.pipeline = rs.pipeline()
        config = rs.config()
        
        # Configure depth and color streams with passed parameters
        config.enable_stream(rs.stream.depth, depth_width, depth_height, rs.format.z16, depth_fps)
        config.enable_stream(rs.stream.color, color_width, color_height, rs.format.bgr8, color_fps)
        
        # Start the camera pipeline with the given configurations
        self.pipeline.start(config)
    
    def get_image(self):
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        
        # Check if both frames are available
        if not depth_frame or not color_frame:
            raise RuntimeError('Could not acquire depth or color frames.')
        
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
        # Return the color image, raw depth image, and depth colormap
        return color_image, depth_image, depth_colormap
    
    def stop(self):
        # Stop the camera pipeline
        self.pipeline.stop()
