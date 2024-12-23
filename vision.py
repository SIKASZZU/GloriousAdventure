from variables import UniversalVariables, GameConfig
import pygame
import math

vision_count: bool = True

def find_boxes_in_window():
    UniversalVariables.walls = []

    for vision_blocking_box in UniversalVariables.collision_boxes:  # x, y, width, height, id
        x = vision_blocking_box[0]
        y = vision_blocking_box[1]
        top_left = (x, y)

        x = vision_blocking_box[0] + vision_blocking_box[2]
        y = vision_blocking_box[1] + vision_blocking_box[3]
        bottom_right = (x, y)

        wall = (top_left, bottom_right)
        if wall not in UniversalVariables.walls:
            UniversalVariables.walls.append(wall)

def get_line_segment_intersection(p0, p1, p2, p3):
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
        return (p0[0] + (t * s1_x), p0[1] + (t * s1_y))

    return None  # No collision

def draw_shadows(self, screen, visible_points):
    shadow_color = 0 if UniversalVariables.debug_mode and vision_count == True else 255

    self.shadow_mask = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    self.shadow_mask.fill((0, 0, 0, shadow_color))

    player_x_row = int(UniversalVariables.player_x // UniversalVariables.block_size)
    player_y_col = int(UniversalVariables.player_y // UniversalVariables.block_size)

    UniversalVariables.light_range = UniversalVariables.base_light_range
    UniversalVariables.opposite_light_range = UniversalVariables.base_opposite_light_range
    player_cone_light_strenght = self.daylight_strength

    try:
        if self.terrain_data[player_y_col][player_x_row] not in GameConfig.RENDER_RANGE_SMALL.value:
            UniversalVariables.light_range *= 6
            UniversalVariables.opposite_light_range *= 34
            if self.terrain_data[player_y_col][player_x_row] not in {988, 9882, 500, 550, 555}:
                player_cone_light_strenght -= 100

    except IndexError as e: 
        print('Error @ vision.py, draw_shadows:', e)
        
    if UniversalVariables.current_equipped_item == 'Flashlight':  
        player_cone_light_strenght -= 70
    if player_cone_light_strenght < 0:  
        player_cone_light_strenght = 0
    
    vertices = [(int(x), int(y)) for x, y in visible_points]
    pygame.draw.polygon(self.shadow_mask, (0, 0, 0, player_cone_light_strenght), vertices)

    squares_hit = set()
    for wall in UniversalVariables.walls:
        for point in visible_points:
            if wall[0][0] <= point[0] <= wall[1][0] and wall[0][1] <= point[1] <= wall[1][1]:
                squares_hit.add(wall)

    for square in squares_hit:
        walls_hit_by_ray_color = player_cone_light_strenght
        pygame.draw.rect(self.shadow_mask, (0, 0, 0, walls_hit_by_ray_color), 
                        pygame.Rect(square[0], (square[1][0] - square[0][0], square[1][1] - square[0][1])))

    screen.blit(self.shadow_mask, (0, 0))

def get_relevant_segments(wall, player_pos):
    # Determine which two segments are relevant based on the player's position
    corners = [
        (wall[0][0], wall[0][1]),
        (wall[1][0], wall[0][1]),
        (wall[1][0], wall[1][1]),
        (wall[0][0], wall[1][1])
    ]
    
    mid_x = (wall[0][0] + wall[1][0]) / 2
    mid_y = (wall[0][1] + wall[1][1]) / 2
    
    if player_pos[0] < mid_x:  # Player is to the left of the wall
        if player_pos[1] < mid_y:  # Player is above the wall
            relevant_segments = [(corners[0], corners[1]), (corners[0], corners[3])]
        else:  # Player is below the wall
            relevant_segments = [(corners[0], corners[3]), (corners[2], corners[3])]
    else:  # Player is to the right of the wall
        if player_pos[1] < mid_y:  # Player is above the wall
            relevant_segments = [(corners[0], corners[1]), (corners[1], corners[2])]
        else:  # Player is below the wall
            relevant_segments = [(corners[1], corners[2]), (corners[2], corners[3])]
    
    return relevant_segments


def draw_ray(screen, ray, color, width):
    pygame.draw.line(screen, color, ray[0], ray[1], width)



main_global     = None
opposite_global = None
def draw_light_source_and_rays(self, screen, position):
    global opposite_global
    global main_global

    # funci sisesed variables
    light_source = position
    visible_points = []
    vision_step = 5
    attack_key_tuple = UniversalVariables.attack_key_pressed[1]
    
    if UniversalVariables.attack_key_pressed[0] == True:  # [0] bool TRUE if pressed, [1] tuple, and which arrow key is pressed: up, down, left, right
        
        # tra see last inputi settimine siin pole yldse loogiilne aga nii t66tab. idk wtf
        if attack_key_tuple[1] == True:  UniversalVariables.last_input = 's'
        elif attack_key_tuple[2] == True:  UniversalVariables.last_input = 'a'
        elif attack_key_tuple[3] == True:  UniversalVariables.last_input = 'd'
        else:                            UniversalVariables.last_input = 'w'

    if len(UniversalVariables.last_input) >= 3 and main_global == None:
        main_angles = range(0, 360 + vision_step)
        opposite_angles = range(0, 0)

    elif main_global != None and UniversalVariables.last_input == "None":
        main_angles = main_global
        opposite_angles = opposite_global
    
    elif UniversalVariables.last_input == 'wa':
        main_angles = range(135, 315)
        opposite_angles = range(310, 500)
    elif UniversalVariables.last_input == 'wd':
        main_angles = range(-135, 45)
        opposite_angles = range(40, 230)
    elif UniversalVariables.last_input == 'sa':
        main_angles = range(45, 225)
        opposite_angles = range(220, 410)
    elif UniversalVariables.last_input == 'sd':
        main_angles = range(-45, 135)
        opposite_angles = range(130, 320)
    
    elif UniversalVariables.last_input == 'w':
        main_angles = range(205, 335)
        opposite_angles = range(335, 566)
    elif UniversalVariables.last_input == 's':
        main_angles = range(25, 155)
        opposite_angles = range(155, 386)
    elif UniversalVariables.last_input == 'a':
        main_angles = range(125, 245)
        opposite_angles = range(245, 486)
    elif UniversalVariables.last_input == 'd':
        main_angles = range(295, 415)
        opposite_angles = range(415, 656)

    # Kui hoiad kõiki key'si all
    else: opposite_angles, main_angles = range(0, 360), range(0, 360)

    opposite_global = opposite_angles
    main_global = main_angles

    def calculate_angle(main_angles, opposite_angles):
        #TODO: fix this lag please lord help 
        light_range = UniversalVariables.light_range
        lowest_angle = min(main_angles.start, opposite_angles.start)
        biggest_angle = max(main_angles.stop, opposite_angles.stop)
        
        for angle in range(lowest_angle, biggest_angle, vision_step):
            if angle in opposite_angles: 
                light_range = UniversalVariables.opposite_light_range
                
            rad_angle = math.radians(angle)
            ray_end = (light_source[0] + math.cos(rad_angle) * light_range,
                       light_source[1] + math.sin(rad_angle) * light_range)

            closest_intersection = None
                        
            for wall in UniversalVariables.walls:
                relevant_segments = get_relevant_segments(wall, light_source)
                for seg_start, seg_end in relevant_segments:
                    intersection = get_line_segment_intersection(light_source, ray_end, seg_start, seg_end)
                    if intersection:
                        if closest_intersection is None or math.hypot(intersection[0] - light_source[0], intersection[1] - light_source[1]) < math.hypot(closest_intersection[0] - light_source[0], closest_intersection[1] - light_source[1]):
                                closest_intersection = intersection

            if closest_intersection:
                distance_to_intersection = math.hypot(closest_intersection[0] - light_source[0], closest_intersection[1] - light_source[1])
                if distance_to_intersection <= light_range:
                    if closest_intersection not in visible_points:
                        visible_points.append(closest_intersection)
                    #if UniversalVariables.debug_mode == True:  draw_ray(screen, (light_source, closest_intersection), (255, 255, 255), 1)  # Draw the ray
            else:
                if closest_intersection not in visible_points:
                    visible_points.append(ray_end)
                #if UniversalVariables.debug_mode == True:  draw_ray(screen, (light_source, ray_end), (255, 0, 255), 1)

        return visible_points
    
    visible_points = calculate_angle(main_angles, opposite_angles)
    if len(visible_points) > 2:  draw_shadows(self, screen, visible_points)
