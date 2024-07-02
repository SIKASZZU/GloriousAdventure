import pygame
import math
import os
import sys

import vision
from images import ImageLoader
from HUD import HUD_class
from inventory import Inventory
from sprite import AnimationManager
from sprite import load_sprite_sheets
from components import StaminaComponent, HungerComponent
from variables import UniversalVariables


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PlayerUpdate:
    # ******************** ANIMATION ******************** #
    sprite_sheets, animations = load_sprite_sheets([
        resource_path('images/Player/Left.png'), 
        resource_path('images/Player/Right.png'), 
        resource_path('images/Player/Up.png'), 
        resource_path('images/Player/Down.png')
    ])

    sprite_sheets_idle, animations_idle = load_sprite_sheets([
        resource_path('images/Player/Idle_Left.png'), 
        resource_path('images/Player/Idle_Right.png'), 
        resource_path('images/Player/Idle_Up.png'), 
        resource_path('images/Player/Idle_Down.png')
    ])

    # *** swimming *** #
    sprite_sheets_swimming, animations_swimming = load_sprite_sheets([
        resource_path('images/Player/Swim/Left_swimming.png'), 
        resource_path('images/Player/Swim/Right_swimming.png'), 
        resource_path('images/Player/Swim/Up_swimming.png'), 
        resource_path('images/Player/Swim/Down_swimming.png')
    ])

    sprite_sheets_idle_swimming, animations_idle_swimming = load_sprite_sheets([
        resource_path('images/Player/Swim/Idle_Left_swimming.png'), 
        resource_path('images/Player/Swim/Idle_Right_swimming.png'), 
        resource_path('images/Player/Swim/Idle_Up_swimming.png'), 
        resource_path('images/Player/Swim/Idle_Down_swimming.png')
    ])


    animation_speeds = [10, 10, 10, 10]

    # Teeb idle ja mitte idle animatsioone
    animation_manager = AnimationManager(sprite_sheets, animations, animation_speeds)
    idle_animation_manager = AnimationManager(sprite_sheets_idle, animations_idle,
                                                    animation_speeds)

    # *** swimming *** #
    swimming_animation_manager = AnimationManager(sprite_sheets_swimming, animations, animation_speeds)
    idle_swimming_animation_manager = AnimationManager(sprite_sheets_idle_swimming, animations_idle,
                                                    animation_speeds)

    def update_player(self) -> None:
        """ Uuendab player datat (x,y ja animation väärtused) ja laseb tal liikuda. """
        if UniversalVariables.cutscene:  # Check if cutscene is active
            keys = pygame.key.get_pressed()  # Track keyboard inputs

            self.animation_index = 2  # Up animation
            UniversalVariables.last_input = 'w'

            x = 0 * int(keys[pygame.K_a]) + 0 * int(keys[pygame.K_d])
            y = 0 * int(keys[pygame.K_w]) + 0 * int(keys[pygame.K_s])


            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Handle pressing Escape during cutscene
                    UniversalVariables.cutscene = False  # Deactivate cutscene


        else:
            keys = pygame.key.get_pressed()  # Track keyboard inputs

            # Teeb uue player x/y, algne x ja y tuleb playeri maailma panekuga (randint)
            new_player_x: int = UniversalVariables.player_x
            new_player_y: int = UniversalVariables.player_y

            if keys[pygame.K_LSHIFT]:
                self.frame_delay = 10  # Adjust running speed
                if keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d] or keys[pygame.K_w]:
                    if self.player.stamina.current_stamina >= 2:
                        HungerComponent.hunger_timer += 2
            else:
                self.frame_delay = 7  # Default walking speed
            if keys[pygame.K_d]:
                self.animation_index = 1  # Right animation
                UniversalVariables.last_input = 'd'
            if keys[pygame.K_a]:
                self.animation_index = 0  # Left animation
                UniversalVariables.last_input = 'a'
            if keys[pygame.K_s]:
                self.animation_index = 3  # Down animation
                UniversalVariables.last_input = 's'
                if keys[pygame.K_a]: UniversalVariables.last_input += 'a'
                if keys[pygame.K_d]: UniversalVariables.last_input += 'd'
            if keys[pygame.K_w]:
                self.animation_index = 2  # Up animation
                UniversalVariables.last_input = 'w'
                if keys[pygame.K_a]: UniversalVariables.last_input += 'a'
                if keys[pygame.K_d]: UniversalVariables.last_input += 'd'

            x = -1 * int(keys[pygame.K_a]) + 1 * int(keys[pygame.K_d])
            y = -1 * int(keys[pygame.K_w]) + 1 * int(keys[pygame.K_s])


        # diagonaalspeedi kontrollimine. Selle funktsionaalsus tundub 6ige, aga ingame doesn't feel right... FPS influence maybe
        magnitude = math.sqrt(x ** 2 + y ** 2)
        if magnitude == 0:
            normalized_x, normalized_y = 0, 0  # Avoid division by zero
        else:
            normalized_x = x / magnitude
            normalized_y = y / magnitude

        new_player_x = UniversalVariables.player_x + self.player.speed.current_speed * normalized_x
        new_player_y = UniversalVariables.player_y + self.player.speed.current_speed * normalized_y

        if self.player.health.get_health() == 0 and UniversalVariables.debug_mode == False:
            UniversalVariables.last_input = 'None'
        else:
            UniversalVariables.player_x: int = new_player_x
            UniversalVariables.player_y: int = new_player_y

        self.player_rect = pygame.Rect(UniversalVariables.player_x + UniversalVariables.player_hitbox_offset_x,
                                    UniversalVariables.player_y + UniversalVariables.player_hitbox_offset_y,
                                    (UniversalVariables.player_width // 2), (UniversalVariables.player_height // 2))

        # Kui player seisab (Animationi jaoks - IDLE)
        is_idle = not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_e])
        try:
            top_left = self.terrain_data[int((self.player_rect.top + self.player_rect.height) // UniversalVariables.block_size)][int((self.player_rect.left + self.player_rect.width) // UniversalVariables.block_size)]
            top_right = self.terrain_data[int((self.player_rect.top + self.player_rect.height) // UniversalVariables.block_size)][int(self.player_rect.left // UniversalVariables.block_size)]
            bottom_left = self.terrain_data[int(self.player_rect.top // UniversalVariables.block_size)][int((self.player_rect.left + self.player_rect.width) // UniversalVariables.block_size)]
            bottom_right = self.terrain_data[int(self.player_rect.top // UniversalVariables.block_size)][int(self.player_rect.left // UniversalVariables.block_size)]

            if UniversalVariables.last_input != 'None':
                if top_left == 0 and top_right == 0 and bottom_left == 0 and bottom_right == 0:
                    if is_idle:
                        self.frame = PlayerUpdate.idle_swimming_animation_manager.update_animation(keys, is_idle)
                    else:
                        self.frame = PlayerUpdate.swimming_animation_manager.update_animation(keys, is_idle)
                else:
                    if is_idle:
                        self.frame = PlayerUpdate.idle_animation_manager.update_animation(keys, is_idle)
                    else:
                        self.frame = PlayerUpdate.animation_manager.update_animation(keys, is_idle)
            else:  pass
        except Exception as e: print(f'Error @ update.py: {e}')


    def render_player(self) -> None:
        """ Renderib ainult playeri. """

        # Muudab playeri asukohta vastavalt kaamera asukohale / paiknemisele
        player_position_adjusted: tuple[int, int] = (UniversalVariables.player_x + UniversalVariables.offset_x, UniversalVariables.player_y + UniversalVariables.offset_y)

        blit_operations = [
            (self.frame, player_position_adjusted)
            # Add other blit operations here if they exist in the same rendering context.
        ]

        if UniversalVariables.cutscene == False:
            UniversalVariables.screen.blits(blit_operations, doreturn=False)

        # Joonistab playeri ümber punase ringi ehk playeri hitboxi
        player_rect = pygame.Rect(player_position_adjusted[0] + UniversalVariables.player_hitbox_offset_x,
                                  player_position_adjusted[1] + UniversalVariables.player_hitbox_offset_y,
                                  UniversalVariables.player_width * 0.47, UniversalVariables.player_height * 0.74)
        self.player_rect = player_rect


        if UniversalVariables.portal_list != []:
            x, y = int(UniversalVariables.portal_list[0][0]), int(UniversalVariables.portal_list[0][1])
            UniversalVariables.portal_frame_rect = pygame.Rect(x + UniversalVariables.offset_x,
                                                           y + UniversalVariables.offset_y,
                                                           UniversalVariables.block_size, UniversalVariables.block_size)

        # renderib playeri hitboxi
        if (UniversalVariables.render_boxes_counter % 2) != 0 and UniversalVariables.debug_mode:
            pygame.draw.rect(UniversalVariables.screen, (255, 0, 0), self.player_rect, 2)

            if UniversalVariables.portal_list != []:
                pygame.draw.rect(UniversalVariables.screen, "orange", UniversalVariables.portal_frame_rect, 2)


    def render_HUD(self) -> None:
        """ Renderib HUDi (Stamina-, food- ja healthbari). """
        stamina_rect, stamina_bar_border, stamina_bar_bg, \
            health_rect, health_bar_border, health_bar_bg, \
            food_rect, food_bar_border, food_bar_bg, \
            heart_w_midpoint, heart_h_midpoint, food_w_midpoint, food_h_midpoint, \
            hydration_rect, hydration_bar_border, hydration_bar_bg, hydration_w_midpoint, hydration_h_midpoint = HUD_class.bar_visualization(self)
        
        # Renderib stamina-bari
        pygame.draw.rect(UniversalVariables.screen, '#273F87', stamina_bar_bg, 0, 7)
        pygame.draw.rect(UniversalVariables.screen, '#4169E1', stamina_rect, 0, 7)
        pygame.draw.rect(UniversalVariables.screen, 'black', stamina_bar_border, 3, 7)

        # Renderib health-bari
        pygame.draw.rect(UniversalVariables.screen, '#662828', health_bar_bg, 0, 7)
        pygame.draw.rect(UniversalVariables.screen, '#FF6666', health_rect, 0, 7)
        pygame.draw.rect(UniversalVariables.screen, 'black', health_bar_border, 3, 7)
        
        # Renderib food-bari
        pygame.draw.rect(UniversalVariables.screen, '#78684B', food_bar_bg, 0, 7)
        pygame.draw.rect(UniversalVariables.screen, '#C8AE7D', food_rect, 0, 7)
        pygame.draw.rect(UniversalVariables.screen, 'black', food_bar_border, 3, 7)

        # Renderib hydration-bari
        pygame.draw.rect(UniversalVariables.screen, '#071952', hydration_bar_bg, 0, 7)
        pygame.draw.rect(UniversalVariables.screen, '#4a6daf', hydration_rect, 0, 7)
        pygame.draw.rect(UniversalVariables.screen, 'black', hydration_bar_border, 3, 7)

        # Health bari keskele icon (Heart.png)
        heart_icon = ImageLoader.load_gui_image("Health")
        scaled_heart_icon = pygame.transform.scale(heart_icon, (50, 50))
        UniversalVariables.screen.blit(scaled_heart_icon, (heart_w_midpoint, heart_h_midpoint))
        
        # Food bari keskele icon (Food.png)
        food_icon = ImageLoader.load_gui_image("Food")
        scaled_food_icon = pygame.transform.scale(food_icon, (50, 45))
        UniversalVariables.screen.blit(scaled_food_icon, (food_w_midpoint, food_h_midpoint))

        # Food bari keskele icon (Food.png)
        hydration_icon = ImageLoader.load_gui_image("Hydration")
        scaled_hydration_icon = pygame.transform.scale(hydration_icon, (50, 40))
        UniversalVariables.screen.blit(scaled_hydration_icon, (hydration_w_midpoint, hydration_h_midpoint))

class EssentialsUpdate:
        
    game_start_clock = (9, 0)
    time_update: int = 0
    game_day_count = 0
    day_night_text = 'Day'

    # Function to calculate in-game time
    def calculate_time(self):
        if UniversalVariables.debug_mode == True:  game_minute_lenght = 5  # mida väiksem,seda kiiremini aeg mängus möödub
        else:  game_minute_lenght = 75  # mida väiksem,seda kiiremini aeg mängus möödub
        day_night_text = EssentialsUpdate.day_night_text

        time = EssentialsUpdate.game_start_clock  # (9, 0)
        days = EssentialsUpdate.game_day_count
        hours = time[0]
        minutes = time[1]

        # Check if new minute should be added to game's time
        if game_minute_lenght <= EssentialsUpdate.time_update:
            minutes += 1
            EssentialsUpdate.time_update = 0
        
        # Update minutes -> hours, hours -> reset hours, minutes & add days
        if 60 <= minutes:
            hours += 1
            minutes = 0
        if 24 <= hours:
            hours = 0
            minutes = 0
            days += 1

        # Update variables
        EssentialsUpdate.time_update += 1
        EssentialsUpdate.game_day_count = days
        EssentialsUpdate.game_start_clock = (hours, minutes)

        # Update day, night text next to game_day_count
        
        if hours < 8 or hours >= 22: 
            day_night_text = 'Night'
        else: 
            day_night_text = 'Day'
        EssentialsUpdate.day_night_text = day_night_text

        if len(str(minutes)) == 1: minutes = f'0{minutes}'  # alati 2 nubrit minutite kohal
        return hours, minutes, days
    

    def calculate_daylight_strength(self):
        """ See func edastab self.daylight_strengthi vision draw_shadowile."""
        """ Draw_shadowis player_vision_conei valgustugevus self.daylight_strengthist """

        if UniversalVariables.debug_mode == False:
            hours = EssentialsUpdate.game_start_clock[0]  # Get current time

            # calculate daylight strength every interval
            if 20 <= hours < 21: self.daylight_strength = 90  # Evening (20 PM to 20:59 PM)
            if 21 <= hours < 22: self.daylight_strength = 125
            elif 22 <= hours <= 23: self.daylight_strength = 175
            elif 0 <= hours < 2: self.daylight_strength = 235
            elif 2 <= hours < 5: self.daylight_strength = 215
            elif 5 <= hours < 7: self.daylight_strength = 180
            elif 7 <= hours < 8: self.daylight_strength = 110
            elif 8 <= hours < 9: self.daylight_strength = 100  # Dawn (8 AM to 9:59 AM) 
            else: self.daylight_strength = 100


    def check_pressed_keys(self):
        if UniversalVariables.debug_mode == True:

            keys = pygame.key.get_pressed()

            # H key, HITBOX KEY
            if keys[pygame.K_h] and not self.h_pressed:
                self.h_pressed = True
                UniversalVariables.render_boxes_counter += 1
            elif not keys[pygame.K_h]: self.h_pressed = False

            # J KEY, LIGHT ON/OFF KEY
            if keys[pygame.K_j] and not self.j_pressed:
                self.j_pressed = True
                vision.vision_count += 1
            elif not keys[pygame.K_j]: self.j_pressed = False


    def render_gui_text(self, text, position, color=(100, 255, 100), debug=False):
        """Utility function to render text on the screen."""
        if debug == False:
            text_surface = self.font.render(text, True, color)
            UniversalVariables.text_sequence.append((text_surface, position))
        if UniversalVariables.debug_mode == True:
            text_surface = self.font.render(text, True, color)
            UniversalVariables.text_sequence.append((text_surface, position))


    def render_general(self):
        ui_elements = [
            (f"{int(self.clock.get_fps())}", (5, 5)),  # FPS display
            (f"Time {EssentialsUpdate.calculate_time(self)[0]}:{EssentialsUpdate.calculate_time(self)[1]}", (5, 35)),  # Time display
            (f"{EssentialsUpdate.day_night_text} {EssentialsUpdate.calculate_time(self)[2]}", (5, 65)),  # Time display

            ("H - Show hitboxes", (UniversalVariables.screen_x / 2, 5), "orange", True),  # Example with specified position and color
            ("J - Switch light", (UniversalVariables.screen_x / 2, 35), "orange", True),  # Example with specified position and color
            ("TODO list:", (5, UniversalVariables.screen_y - 350), "orange", True),  # Example with specified position and color
            ("Maze mobs - spider.", (10, UniversalVariables.screen_y - 300), "orange", True),  # Example with specified position and color
            ("Maze geiger? / Blade maze.", (10, UniversalVariables.screen_y - 270), "orange", True),  # Example with specified position and color
            ("Final maze asja edasi teha.", (10, UniversalVariables.screen_y - 240), "orange", True),  # Example with specified position and color
            ("Itemite ülesvõtmise delay,", (10, UniversalVariables.screen_y - 210), "orange", True),
            ("breaking animation vms teha.", (10, UniversalVariables.screen_y - 190), "orange", True),
            ("Note'id, et player oskas midagi teha,", (10, UniversalVariables.screen_y - 160), "orange", True),
            ("press 'TAB' to open inventory vms...", (10, UniversalVariables.screen_y - 130), "orange", True),
            ("Selected item ---- Ilusamaks tegema", (10, UniversalVariables.screen_y - 100), "orange", True),
            ("Max item stack - 99  +maze = - key    pickup delay - animation", (10, UniversalVariables.screen_y - 70), "orange", True),

            # Example with specified position and color

        ]

        for element in ui_elements:
            text = element[0]
            position = element[1] if len(element) > 1 else None
            color = element[2] if len(element) > 2 else (100, 255, 100)  # Default color white if not specified
            if len(element) == 4:
                debug_mode = element[3]

            # Call the improved render_text function with the specified parameters
                EssentialsUpdate.render_gui_text(self, text, position=position, color=color, debug=debug_mode)
            else:
                EssentialsUpdate.render_gui_text(self, text, position=position, color=color)
