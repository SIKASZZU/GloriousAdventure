from variables import UniversalVariables
import pygame
import math

# Define walls as rectangles
drawing_wall = False
start_wall_pos = None
light_range = UniversalVariables.light_range  # Range of the light source
vision_count: int = 0
transparent_boxes = []

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
        else:
            transparent_boxes.append(vision_blocking_box)  # box, millel puudub collision, puudub shadow.


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


def draw_shadows(self, screen, visible_points):
    shadow_color = 0
    walls_hit_by_ray_color = 0
    BLOCK_SIZE = UniversalVariables.block_size
    no_shadow_needed = UniversalVariables.no_shadow_needed

    # kas J - Light ON/OFF key on pressed
    if (vision_count % 2) != 0:
        shadow_color = 255
        walls_hit_by_ray_color = 150

    # Create a shadow mask covering the entire screen
    shadow_mask = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  # Use SRCALPHA for per-pixel alpha

    # Fill the shadow mask with shadow color
    shadow_mask.fill((0, 0, 0, shadow_color))

    # Playeri gridi arvutamine
    player_x_row = int(UniversalVariables.player_x // BLOCK_SIZE)
    player_y_col = int(UniversalVariables.player_y // BLOCK_SIZE)

    UniversalVariables.light_range = 420
    UniversalVariables.opposite_light_range = 75
    changed = 100
    try:
        if self.terrain_data[player_y_col][player_x_row] in no_shadow_needed:
            UniversalVariables.light_range *= 6
            UniversalVariables.opposite_light_range *= 34
            changed = 0
    
    except IndexError as e: 
        print('Error @ vision.py, draw_shadows:', e)

    vertices = [(int(x), int(y)) for x, y in visible_points]
    pygame.draw.polygon(shadow_mask, (0, 0, 0, changed), vertices)  # visioni joonestamine

    # Get the squares hit by light rays
    squares_hit = set()
    for wall in UniversalVariables.walls:
        for point in visible_points:
            if wall[0][0] <= point[0] <= wall[1][0] and wall[0][1] <= point[1] <= wall[1][1]:
                squares_hit.add(wall)

    # Highlight wallid, mis saavad rayga pihta
    for square in squares_hit:
        pygame.draw.rect(shadow_mask, (0, 0, 0, walls_hit_by_ray_color), \
                         pygame.Rect(square[0], (square[1][0] - square[0][0], square[1][1] - square[0][1])))

    # Blit the shadow mask onto the screen
    screen.blit(shadow_mask, (0, 0))


def draw_light_source_and_rays(self, screen, position, light_range):
    light_source = position
    visible_points = []
    vision_step = 5

    if len(UniversalVariables.last_input) == 3:
        main_angles = range(0, 360 + vision_step)
        opposite_angles = range(0, 0)
    
    elif UniversalVariables.last_input == 'wa':
        main_angles = range(135, 315)
        opposite_angles = range(-50, 140)
    elif UniversalVariables.last_input == 'wd':
        main_angles = range(-135, 45)
        opposite_angles = range(40, 230)
    elif UniversalVariables.last_input == 'sa':
        main_angles = range(45, 225)
        opposite_angles = range(-140, 50)
    elif UniversalVariables.last_input == 'sd':
        main_angles = range(-45, 135)
        opposite_angles = range(130, 320)
    
    elif UniversalVariables.last_input == 'w':
        main_angles = range(-155, -25)
        opposite_angles = range(-30, 210)
    elif UniversalVariables.last_input == 's':
        main_angles = range(25, 155)
        opposite_angles = range(-210, 30)
    elif UniversalVariables.last_input == 'a':
        main_angles = range(125, 245)
        opposite_angles = range(240, 490)
    elif UniversalVariables.last_input == 'd':
        main_angles = range(-65, 65)
        opposite_angles = range(60, 300)
    else:
        main_angles = range(0, 360 + vision_step)
        opposite_angles = range(0, 0)

    def calculate_angle(requested_angle, light_range):
    
        for angle in range(requested_angle.start, requested_angle.stop, vision_step):
            rad_angle = math.radians(angle)
            ray_end = (light_source[0] + math.cos(rad_angle) * light_range,
                        light_source[1] + math.sin(rad_angle) * light_range)

            closest_intersection = None
            for wall in UniversalVariables.walls:
                corners = [(wall[0][0], wall[0][1]), (wall[1][0], wall[0][1]), (wall[1][0], wall[1][1]), (wall[0][0], wall[1][1])]

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

        visible_points.insert(0, light_source)
        visible_points.append(light_source)

    calculate_angle(main_angles, light_range)
    calculate_angle(opposite_angles, (UniversalVariables.opposite_light_range))
    
    
    # Step 4: Draw shadows and walls as per the existing code
    draw_shadows(self, screen, visible_points)