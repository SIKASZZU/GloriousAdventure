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
    for angle in range(0, 360, 5):
        rad_angle = math.radians(angle)
        ray_dir = (math.cos(rad_angle), math.sin(rad_angle))
        ray_end = (light_source[0] + ray_dir[0] * light_range, light_source[1] + ray_dir[1] * light_range)

        closest_intersection = None
        for wall in UniversalVariables.walls:
            # Convert the rectangle wall to its four edges
            corners = [(wall[0][0], wall[0][1]), (wall[1][0], wall[0][1]), (wall[1][0], wall[1][1]),
                       (wall[0][0], wall[1][1])]
            segments = [(corners[i], corners[(i + 1) % 4]) for i in range(4)]

            for seg_start, seg_end in segments:
                intersection = get_line_segment_intersection(light_source, ray_end, seg_start, seg_end)
                if intersection:
                    if not closest_intersection or math.hypot(intersection[0] - light_source[0],
                                                              intersection[1] - light_source[1]) < math.hypot(
                            closest_intersection[0] - light_source[0], closest_intersection[1] - light_source[1]):
                        closest_intersection = intersection

        if closest_intersection:
            pygame.draw.line(screen, pygame.Color('black'), light_source, closest_intersection, 3)
        else:
            pygame.draw.line(screen, pygame.Color('gray'), light_source, ray_end, 3)
