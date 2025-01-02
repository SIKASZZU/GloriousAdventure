import pygame
import math

class Vision:
    def __init__(self, screen, td, dls, variables, RENDER_RANGE_SMALL):
        self.screen = screen
        self.daylight_strength = dls
        self.terrain_data = td
        self.RENDER_RANGE_SMALL = RENDER_RANGE_SMALL

        self.visible_points  = []
        self.main_global     = None
        self.opposite_global = None
        self.vision_count: bool = True
        self.vision_step = 5
        self.variables = variables

    def find_boxes_in_window(self) -> None:
        self.variables.walls = []

        for vision_blocking_box in self.variables.collision_boxes:  # x, y, width, height, id
            x = vision_blocking_box[0]
            y = vision_blocking_box[1]
            top_left = (x, y)

            x = vision_blocking_box[0] + vision_blocking_box[2]
            y = vision_blocking_box[1] + vision_blocking_box[3]
            bottom_right = (x, y)

            wall = (top_left, bottom_right)
            if wall not in self.variables.walls:
                self.variables.walls.append(wall)

    @staticmethod
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
    
    @staticmethod
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


    def draw_light_source_and_rays(self):

        # funci sisesed variables
        attack_key_tuple = self.variables.attack_key_pressed[1]
        
        if self.variables.attack_key_pressed[0] == True:  # [0] bool TRUE if pressed, [1] tuple, and which arrow key is pressed: up, down, left, right
            
            # tra see last inputi settimine siin pole yldse loogiilne aga nii t66tab. idk wtf
            if attack_key_tuple[1] == True:  self.variables.last_input = 's'
            elif attack_key_tuple[2] == True:  self.variables.last_input = 'a'
            elif attack_key_tuple[3] == True:  self.variables.last_input = 'd'
            else:                            self.variables.last_input = 'w'

        if len(self.variables.last_input) >= 3 and self.main_global == None:
            main_angles = range(0, 360 + self.vision_step)
            opposite_angles = range(0, 0)

        elif self.main_global != None and self.variables.last_input == "None":
            main_angles = self.main_global
            opposite_angles = self.opposite_global
        
        elif self.variables.last_input == 'wa':
            main_angles = range(135, 315)
            opposite_angles = range(310, 500)
        elif self.variables.last_input == 'wd':
            main_angles = range(-135, 45)
            opposite_angles = range(40, 230)
        elif self.variables.last_input == 'sa':
            main_angles = range(45, 225)
            opposite_angles = range(220, 410)
        elif self.variables.last_input == 'sd':
            main_angles = range(-45, 135)
            opposite_angles = range(130, 320)
        
        elif self.variables.last_input == 'w':
            main_angles = range(205, 335)
            opposite_angles = range(335, 566)
        elif self.variables.last_input == 's':
            main_angles = range(25, 155)
            opposite_angles = range(155, 386)
        elif self.variables.last_input == 'a':
            main_angles = range(125, 245)
            opposite_angles = range(245, 486)
        elif self.variables.last_input == 'd':
            main_angles = range(295, 415)
            opposite_angles = range(415, 656)

        # Kui hoiad kõiki key'si all
        else: opposite_angles, main_angles = range(0, 360), range(0, 360)

        self.opposite_global = opposite_angles
        self.main_global = main_angles
        return main_angles, opposite_angles

    def calculate_angle(self, main_angles, opposite_angles, position):
        self.visible_points = []  # reset point list
        #TODO: fix this lag please lord help 
        light_range = self.variables.light_range
        lowest_angle = min(main_angles.start, opposite_angles.start)
        biggest_angle = max(main_angles.stop, opposite_angles.stop)
        
        for angle in range(lowest_angle, biggest_angle, self.vision_step):
            if angle in opposite_angles: 
                light_range = self.variables.opposite_light_range
                
            rad_angle = math.radians(angle)
            ray_end = (position[0] + math.cos(rad_angle) * light_range,
                    position[1] + math.sin(rad_angle) * light_range)

            closest_intersection = None
                        
            for wall in self.variables.walls:
                relevant_segments = Vision.get_relevant_segments(wall, position)
                for seg_start, seg_end in relevant_segments:
                    intersection = Vision.get_line_segment_intersection(position, ray_end, seg_start, seg_end)
                    if intersection:
                        if closest_intersection is None or math.hypot(intersection[0] - position[0], intersection[1] - position[1]) < math.hypot(closest_intersection[0] - position[0], closest_intersection[1] - position[1]):
                                closest_intersection = intersection

            if closest_intersection:
                distance_to_intersection = math.hypot(closest_intersection[0] - position[0], closest_intersection[1] - position[1])
                if distance_to_intersection <= light_range:
                    if closest_intersection not in self.visible_points:
                        self.visible_points.append(closest_intersection)
            else:
                if closest_intersection not in self.visible_points:
                    self.visible_points.append(ray_end)

        return self.visible_points
    

    def draw_shadows(self):
        if len(self.visible_points) < 3:
            return

        shadow_color = 0 if self.variables.debug_mode and self.vision_count == True else 255
        self.shadow_mask = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.shadow_mask.fill((0, 0, 0, shadow_color))

        player_x_row = int(self.variables.player_x // self.variables.block_size)
        player_y_col = int(self.variables.player_y // self.variables.block_size)

        self.variables.light_range = self.variables.base_light_range
        self.variables.opposite_light_range = self.variables.base_opposite_light_range
        player_cone_light_strenght = self.daylight_strength

        try:
            if self.terrain_data[player_y_col][player_x_row] not in self.RENDER_RANGE_SMALL.value:
                self.variables.light_range *= 6
                self.variables.opposite_light_range *= 34
                if self.terrain_data[player_y_col][player_x_row] not in {988, 9882, 500, 550, 555}:
                    player_cone_light_strenght -= 100

        except IndexError as e: 
            print('Error @ vision.py, draw_shadows:', e)
            
        if self.variables.current_equipped_item == 'Flashlight':  
            player_cone_light_strenght -= 70
        if player_cone_light_strenght < 0:  
            player_cone_light_strenght = 0
        
        vertices = [(int(x), int(y)) for x, y in self.visible_points]
        if len(vertices) > 2:
            pygame.draw.polygon(self.shadow_mask, (0, 0, 0, player_cone_light_strenght), vertices)

        squares_hit = set()
        for wall in self.variables.walls:
            for point in self.visible_points:
                if wall[0][0] <= point[0] <= wall[1][0] and wall[0][1] <= point[1] <= wall[1][1]:
                    squares_hit.add(wall)

        for square in squares_hit:
            walls_hit_by_ray_color = player_cone_light_strenght
            pygame.draw.rect(self.shadow_mask, (0, 0, 0, walls_hit_by_ray_color), 
                            pygame.Rect(square[0], (square[1][0] - square[0][0], square[1][1] - square[0][1])))

        self.screen.blit(self.shadow_mask, (0, 0))


    def update(self, position):

        self.find_boxes_in_window()  # List of walls coords on screen
        main_angles, opposite_angles = self.draw_light_source_and_rays()
        self.visible_points = self.calculate_angle(main_angles, opposite_angles, position)
        self.draw_shadows()