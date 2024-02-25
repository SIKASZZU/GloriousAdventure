from variables import UniversalVariables
import pygame
import math

# Define walls as rectangles
drawing_wall = False
start_wall_pos = None
light_range = UniversalVariables.light_range  # Range of the light source

def find_boxes_in_window():
    UniversalVariables.walls = []

    # Need boxid on render rangei sees
    for vision_blocking_box in UniversalVariables.collision_boxes:  # x, y, width, height, id, offset_x, offset_y
        if vision_blocking_box[2] != 0 or vision_blocking_box[3] != 0: # width, height == 0: pass

            x = vision_blocking_box[0] + UniversalVariables.offset_x
            y = vision_blocking_box[1] + UniversalVariables.offset_y
            top_left = (x, y)

            x = vision_blocking_box[0] + vision_blocking_box[2] + UniversalVariables.offset_x
            y = vision_blocking_box[1] + vision_blocking_box[3] + UniversalVariables.offset_y
            bottom_right = (x, y)


            wall = (top_left, bottom_right)
            if wall not in UniversalVariables.walls:
                UniversalVariables.walls.append(wall)


def add_wall(start, end):
    UniversalVariables.walls.append((start, end))


def draw_walls(screen):
    for wall in UniversalVariables.walls:
        pygame.draw.rect(screen, pygame.Color('white'),
                         pygame.Rect(wall[0], (wall[1][0] - wall[0][0], wall[1][1] - wall[0][1])), 1)


def get_line_segment_intersection(p0, p1, p2, p3):
    """
    Returns the point of intersection between two line segments if it exists.
    p0, p1 are the endpoints of the first segment, p2, p3 are the endpoints of the second.
    """
    s1_x = p1[0] - p0[0]
    s1_y = p1[1] - p0[1]
    s2_x = p3[0] - p2[0]
    s2_y = p3[1] - p2[1]

    denom = (-s2_x * s1_y + s1_x * s2_y)
    if denom == 0:
        return None  # Lines are parallel, no intersection

    s = (-s1_y * (p0[0] - p2[0]) + s1_x * (p0[1] - p2[1])) / denom
    t = (s2_x * (p0[1] - p2[1]) - s2_y * (p0[0] - p2[0])) / denom

    if 0 <= s <= 1 and 0 <= t <= 1:  # Intersection detected
        # Collision detected
        return (p0[0] + (t * s1_x), p0[1] + (t * s1_y))

    return None  # No collision


def draw_light_source_and_rays(screen, position, light_range):
    light_source = position
    visible_points = []
    corners_to_check = set()

    # Helper function to check direct visibility of a corner and its distance
    def is_corner_visible_and_within_range(corner):
        direct_ray_end = corner
        distance = math.hypot(corner[0] - light_source[0], corner[1] - light_source[1])
        if distance > light_range:
            return False  # Corner is beyond the light range

        for wall in UniversalVariables.walls:
            corners = [(wall[0][0], wall[0][1]), (wall[1][0], wall[0][1]),
                       (wall[1][0], wall[1][1]), (wall[0][0], wall[1][1])]
            segments = [(corners[i], corners[(i + 1) % 4]) for i in range(4)]
            for seg_start, seg_end in segments:
                if seg_start == corner or seg_end == corner:
                    continue  # Skip the segment that includes the corner itself
                intersection = get_line_segment_intersection(light_source, direct_ray_end, seg_start, seg_end)
                if intersection:
                    # Check if intersection is closer to the light source than the corner
                    if math.hypot(intersection[0] - light_source[0], intersection[1] - light_source[1]) < distance:
                        return False  # Corner is not visible because another wall blocks the view
        return True

    # Step 1: Cast Rays in All Directions
    for angle in range(0, 360, 5):
        rad_angle = math.radians(angle)
        ray_end = (light_source[0] + math.cos(rad_angle) * light_range,
                   light_source[1] + math.sin(rad_angle) * light_range)

        closest_intersection = None
        for wall in UniversalVariables.walls:
            corners = [(wall[0][0], wall[0][1]), (wall[1][0], wall[0][1]),
                       (wall[1][0], wall[1][1]), (wall[0][0], wall[1][1])]
            for corner in corners:
                corners_to_check.add(corner)

            segments = [(corners[i], corners[(i + 1) % 4]) for i in range(4)]
            for seg_start, seg_end in segments:
                intersection = get_line_segment_intersection(light_source, ray_end, seg_start, seg_end)
                if intersection:
                    if closest_intersection is None or \
                            math.hypot(intersection[0] - light_source[0], intersection[1] - light_source[1]) < \
                            math.hypot(closest_intersection[0] - light_source[0], closest_intersection[1] - light_source[1]):
                        closest_intersection = intersection

        # Ensure that the intersection point is within the light range
        if closest_intersection:
            distance_to_intersection = math.hypot(closest_intersection[0] - light_source[0], closest_intersection[1] - light_source[1])
            if distance_to_intersection <= light_range:
                visible_points.append(closest_intersection)
        else:
            visible_points.append(ray_end)

    # Step 2: Check and Cast Rays Only to Visible Corners Within Light Range
    for corner in corners_to_check:
        if is_corner_visible_and_within_range(corner):
            visible_points.append(corner)

    # Step 3: Combine Rays to Form Visibility Polygon
    visible_points = sorted(visible_points, key=lambda x: math.atan2(x[1] - light_source[1], x[0] - light_source[0]))
    pygame.draw.polygon(screen, pygame.Color('yellow'), visible_points, 1)  # Outline for visibility

    # Optionally, fill the polygon for better visual effect
    pygame.draw.polygon(screen, pygame.Color(255, 255, 0, 50), visible_points, 0)
