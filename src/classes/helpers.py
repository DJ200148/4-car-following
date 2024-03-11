import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
from geopy.distance import geodesic
from geopy.point import Point

def calculate_bearing(lat1, lon1, lat2, lon2):
    """
    Calculates the bearing from point 1 to point 2.
    
    Parameters:
    - lat1, lon1: Latitude and longitude of the first point.
    - lat2, lon2: Latitude and longitude of the second point.
    
    Returns:
    - Bearing in degrees.
    """
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    delta_lon = lon2 - lon1

    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon))

    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def calculate_relative_direction(start_lat, start_lon, current_lat, current_lon, end_lat, end_lon):
    """
    Calculates whether to turn left or right from the current position to align
    with the path defined by start and end points, and gives the angle with positive
    for right and negative for left.
    
    Parameters:
    - start_lat, start_lon: Latitude and longitude of the start position.
    - current_lat, current_lon: Latitude and longitude of the current position.
    - end_lat, end_lon: Latitude and longitude of the end position.
    
    Returns:
    - A tuple containing the direction to turn ('LEFT' or 'RIGHT') and the angle in degrees.
      The angle is positive for right turns and negative for left turns.
    """
    # Calculate bearings
    start_to_current_bearing = calculate_bearing(start_lat, start_lon, current_lat, current_lon)
    current_to_end_bearing = calculate_bearing(current_lat, current_lon, end_lat, end_lon)

    # Calculate turn angle
    turn_angle = (current_to_end_bearing - start_to_current_bearing + 360) % 360
    if turn_angle > 180:
        direction = 'LEFT'
        turn_angle = 360 - turn_angle  # Make the angle negative for left turn
        turn_angle *= -1
    else:
        direction = 'RIGHT'  # Angle remains positive for right turn
    
    return (direction, turn_angle)


def get_turn_direction_from_depth_data(depth_image, low_threshold=500, high_threshold=1000):
    h, w = depth_image.shape
    third_w = w // 3
    forth_h = h // 4

    # Divide the depth image into three sections: left, center, and right
    left = depth_image[:, :third_w]
    center = depth_image[:, third_w:2*third_w]
    right = depth_image[:, 2*third_w:]

    bot_left = left[3*forth_h:, :]
    bot_center = center[3*forth_h:, :]
    bot_right = right[3*forth_h:, :]

    top_left = left[:3*forth_h,:]
    top_center = center[:3*forth_h,:]
    top_right = right[:3*forth_h,:]

    # Filter the depth values that are below the threshold for each section
    bot_left_filtered = bot_left[bot_left < low_threshold]
    bot_center_filtered = bot_center[bot_center < low_threshold]
    bot_right_filtered = bot_right[bot_right < low_threshold]

    top_left_filtered = top_left[top_left < high_threshold]
    top_center_filtered = top_center[top_center < high_threshold]
    top_right_filtered = top_right[top_right < high_threshold]

    # Compute the summation of filtered depth values for each section
    bot_left_sum = np.sum(bot_left_filtered)
    bot_center_sum = np.sum(bot_center_filtered)
    bot_right_sum = np.sum(bot_right_filtered)

    top_left_sum = np.sum(top_left_filtered)
    top_center_sum = np.sum(top_center_filtered)
    top_right_sum = np.sum(top_right_filtered)

    # Check if there's an obstacle in the center section
    center_obstacle = top_center_sum > 0 or bot_center_sum > 0
    left_obstacle = top_left_sum > 0 or bot_left_sum > 0
    right_obstacle = top_right_sum > 0 or bot_right_sum > 0
    if center_obstacle:
        # If there's an obstacle in the center, check left and right sections
        if left_obstacle and right_obstacle:
            return 'stop'  # Both sides blocked
        elif left_obstacle:
            return 'right'  # Obstacle on the left
        elif right_obstacle:
            return 'left'  # Obstacle on the right
        else:
            return 'stop'
    else:
        return 'forward'  # Path is clear



def add_lines_to_image(image):
    # Drawing the lines as before
    height, width = image.shape[:2]
    one_third, two_third = width // 3, width * 2 // 3
    three_quarter_height = height * 3 // 4

    # Draw vertical lines
    cv2.line(image, (one_third, 0), (one_third, height), (255, 255, 255), 2)
    cv2.line(image, (two_third, 0), (two_third, height), (255, 255, 255), 2)
    
    # Draw horizontal line
    cv2.line(image, (0, three_quarter_height), (width, three_quarter_height), (255, 255, 255), 2)

    return image