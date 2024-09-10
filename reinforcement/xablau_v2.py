import math

def reward_function(params):
    # Extract parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    steering = abs(params['steering_angle'])
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']

    # Initialize reward
    reward = 1.0

    # 1. Stay within track borders
    if not all_wheels_on_track:
        return 1e-3  # Minimum reward if off track

    # 2. Follow the centerline
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
        return 1e-3  # Likely crashed or close to off track

    # 3. Prevent Zig-Zag by penalizing sharp steering angles
    ABS_STEERING_THRESHOLD = 15.0
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8  # Penalize high steering angles to prevent zig-zag

    # 4. Maintain proper heading
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the track direction
    track_direction = math.degrees(math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]))
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize if the heading is not aligned with the track direction
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    # 5. Encourage moderate speed for balance between speed and control
    SPEED_THRESHOLD = 2.0  # m/s
    if speed > SPEED_THRESHOLD:
        reward += 1.0
    else:
        reward += 0.5

    return float(reward)
        