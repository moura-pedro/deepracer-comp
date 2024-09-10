import math

def reward_function(params):
    # Define constants
    MAX_REWARD = 1e2
    MIN_REWARD = 1e-3
    DIRECTION_THRESHOLD = 10.0
    ABS_STEERING_THRESHOLD = 15.0  # More conservative threshold for smoother steering
    SPEED_THRESHOLD = 2.5

    # Read parameters
    on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle'])
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    progress = params['progress']  # Reward based on how much of the track is completed

    # Initialize reward
    reward = 1.0

    # 1. Reward for staying on the track
    if not on_track:
        return MIN_REWARD

    # 2. Reward based on distance from centerline
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        return MIN_REWARD  # Car is likely off track

    # 3. Penalize sharp steering to prevent zig-zag
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8  # Decrease reward for sharp steering

    # 4. Adjust reward based on heading alignment
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    track_direction = math.degrees(math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]))
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5  # Penalize for significant misalignment

    # 5. Encourage optimal speed
    if speed > SPEED_THRESHOLD:
        reward += 1.0
    else:
        reward += 0.5  # Still give some reward if moving but not too fast

    # 6. Bonus for making progress
    reward += progress * 0.1  # Scales reward based on progress made on the track

    return float(reward)
