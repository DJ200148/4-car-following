import numpy as np

class AlgoDetectionHelper:
    def __init__(self):
        pass

    def proccess_depth_image(self, depth_image):
        pass

    def process_segmentation_image(self, segmentation_image):
        pass
    
    def get_turn_direction_from_depth_data(self, depth_image, threshold=1000):
        h, w = depth_image.shape
        left = depth_image[:, :w//2]
        right = depth_image[:, w//2:]
        
        left_obstacle = np.any(left < threshold)
        right_obstacle = np.any(right < threshold)
        
        if left_obstacle and right_obstacle:
            return 'reverse'  # Both sides blocked
        elif left_obstacle:
            return 'right'  # Obstacle on the left
        elif right_obstacle:
            return 'left'  # Obstacle on the right
        else:
            return 'forward'  # Path is clear
        
    def get_turn_angle_from_depth_data(depth_image, threshold=1000, max_angle=45):
        h, w = depth_image.shape
        left = depth_image[:, :w//2]
        right = depth_image[:, w//2:]

        # Count the number of pixels considered as obstacles in each half
        left_obstacle_count = np.sum(left < threshold)
        right_obstacle_count = np.sum(right < threshold)
        
        # Calculate the total obstacle pixels
        total_obstacles = left_obstacle_count + right_obstacle_count
        
        if total_obstacles > 0:
            # Calculate the difference in obstacle density between the two halves
            balance = (right_obstacle_count - left_obstacle_count) / total_obstacles
            
            # Convert balance to an angle where balance = 1 is max_angle to the right and balance = -1 is max_angle to the left
            turn_angle = balance * max_angle
        else:
            # Path is clear, no need to turn
            turn_angle = 0

        return turn_angle
