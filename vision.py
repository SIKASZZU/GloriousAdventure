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

    # kas J - Light ON/OFF key on pressed
    if (vision_count % 2) != 0:
        shadow_color = 255
        walls_hit_by_ray_color = 150

    ### Shadow maze blockidele
    shadow_mask = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  # Use SRCALPHA for per-pixel alpha
    for wall in UniversalVariables.walls:
        pygame.draw.rect(shadow_mask, (0, 0, 0, shadow_color), \
                            pygame.Rect(wall[0], (wall[1][0] - wall[0][0], wall[1][1] - wall[0][1])))
    
    for y in range(len(self.terrain_data)):
        for x in range(len(self.terrain_data[y])):
            if self.terrain_data[y][x] == 98:
                pathway_rect = pygame.Rect(x * BLOCK_SIZE + UniversalVariables.offset_x, y * BLOCK_SIZE + UniversalVariables.offset_y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(shadow_mask, (0, 0, 0, shadow_color), pathway_rect)

    vertices = [(int(x), int(y)) for x, y in visible_points]
    pygame.draw.polygon(shadow_mask, (0, 0, 0, 0), vertices)  # visioni joonestamine

    # Get the squares hit by light rays
    squares_hit = set()
    for wall in UniversalVariables.walls:
        for point in visible_points:
            if wall[0][0] <= point[0] <= wall[1][0] and wall[0][1] <= point[1] <= wall[1][1]:
                squares_hit.add(wall)

    # Highlightib wallid, mis saavad rayga pihta 
    for square in squares_hit:
        pygame.draw.rect(shadow_mask, (0, 0, 0, walls_hit_by_ray_color), \
                         pygame.Rect(square[0], (square[1][0] - square[0][0], square[1][1] - square[0][1])))

    # Blit the shadow mask onto the screen
    screen.blit(shadow_mask, (0, 0))


def draw_light_source_and_rays(self, screen, position, light_range):
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

    # seda funci pole vaja, aga fancy on. Saaks niisama settida v22rtused.
    def combine_ranges(range1, range2):
        combined_range = range(min(range1.start, range2.start), max(range1.stop, range2.stop))
        return combined_range

    # Define angle ranges based on the player's last input
    # Kui player vajutab kahte nuppu alla, suureneb vision cone
    if UniversalVariables.last_input == 'wa':
        angles = combine_ranges(range(135, 45), range(135, 315))  # tra, need numbrid on forcefully pandud. Teised on 6iged juba by god
    elif UniversalVariables.last_input == 'wd':
        angles = combine_ranges(range(-135, -45), range(-45, 45))
    elif UniversalVariables.last_input == 'sa':
        angles = combine_ranges(range(45, 135), range(135, 225))
    elif UniversalVariables.last_input == 'sd':
        angles = combine_ranges(range(45, 135), range(-45, 45))

    # Kui player vajutab ainult yhte movement nuppu
    elif UniversalVariables.last_input == 'w':
        angles = range(-155, -25)
    elif UniversalVariables.last_input == 's':
        angles = range(25, 155)
    elif UniversalVariables.last_input == 'a':
        angles = range(125, 245)
    elif UniversalVariables.last_input == 'd':
        angles = range(-65, 65)
    else:
        angles = range(0, 360)
    # Step 1: Cast Rays in All Directions
    for angle in range(angles.start, angles.stop, 5):
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

    # # Step 2: Check and Cast Rays Only to Visible Corners Within Light Range
    # for corner in corners_to_check:
    #     if is_corner_visible_and_within_range(corner):
    #         visible_points.append(corner)

    visible_points.insert(0, light_source)
    visible_points.append(light_source)

    # Step 3: Create a polygon to display as the vision system
    pygame.draw.polygon(screen, pygame.Color('yellow'), visible_points, 1) # Outline for visibility

    draw_shadows(self, screen, visible_points)
