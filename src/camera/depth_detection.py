import pyrealsense2 as rs
import numpy as np
import cv2
import os

image_folder = r"E:\OneDrive\Desktop\image"

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)


pipeline.start(config)

try:
    for _ in range(30):
        pipeline.wait_for_frames()

    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    if not depth_frame or not color_frame:
        raise RuntimeError("Could not acquire depth or color frames.")

    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    cv2.imwrite(f'{image_folder}/color_image.jpg', color_image)
    cv2.imwrite(f'{image_folder}/depth_image.jpg', depth_colormap)

    print("Images have been saved.")

finally:
    pipeline.stop()

