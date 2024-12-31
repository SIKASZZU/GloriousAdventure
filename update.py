import pygame
import math
import os
import sys

from sprite import AnimationManager
from sprite import load_sprite_sheets
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
    def __init__(self, terrain_data):
        self.terrain_data = terrain_data

        self.player = None

        # ******************** ANIMATION ******************** #
        self.sprite_sheets, self.animations = load_sprite_sheets([
            resource_path('images/Player/Left.png'),
            resource_path('images/Player/Right.png'),
            resource_path('images/Player/Up.png'),
            resource_path('images/Player/Down.png')
        ])

        self.sprite_sheets_idle, self.animations_idle = load_sprite_sheets([
            resource_path('images/Player/Idle_Left.png'),
            resource_path('images/Player/Idle_Right.png'),
            resource_path('images/Player/Idle_Up.png'),
            resource_path('images/Player/Idle_Down.png')
        ])

        # *** swimming *** #
        self.sprite_sheets_swimming, self.animations_swimming = load_sprite_sheets([
            resource_path('images/Player/Swim/Left_swimming.png'),
            resource_path('images/Player/Swim/Right_swimming.png'),
            resource_path('images/Player/Swim/Up_swimming.png'),
            resource_path('images/Player/Swim/Down_swimming.png')
        ])

        self.sprite_sheets_idle_swimming, self.animations_idle_swimming = load_sprite_sheets([
            resource_path('images/Player/Swim/Idle_Left_swimming.png'),
            resource_path('images/Player/Swim/Idle_Right_swimming.png'),
            resource_path('images/Player/Swim/Idle_Up_swimming.png'),
            resource_path('images/Player/Swim/Idle_Down_swimming.png')
        ])


        self.animation_speeds = [10, 10, 10, 10]

        # Teeb idle ja mitte idle animatsioone
        self.animation_manager = AnimationManager(self.sprite_sheets, self.animations, self.animation_speeds)
        self.idle_animation_manager = AnimationManager(self.sprite_sheets_idle, self.animations_idle,
                                                        self.animation_speeds)

        # *** swimming *** #
        self.swimming_animation_manager = AnimationManager(self.sprite_sheets_swimming, self.animations, self.animation_speeds)
        self.idle_swimming_animation_manager = AnimationManager(self.sprite_sheets_idle_swimming, self.animations_idle, self.animation_speeds)

        self.player_rect = None
        self.frame = None

    @staticmethod
    def disable_movement() -> tuple[int, int]:
        return 0, 0

    def update_player(self, player) -> None:
        self.player = player

        """ Uuendab player datat (x,y ja animation väärtused) ja laseb tal liikuda. """
        keys = pygame.key.get_pressed()  # Track keyboard inputs

        if not UniversalVariables.allow_movement:  # Check if cutscene is active
            x, y = PlayerUpdate.disable_movement()

        else:
            keys = pygame.key.get_pressed()  # Track keyboard inputs

            # Teeb uue player x/y, algne x ja y tuleb playeri maailma panekuga (randint)
            new_player_x: int = UniversalVariables.player_x
            new_player_y: int = UniversalVariables.player_y

            # fixme mis see self.frame delayu on ??

            if keys[pygame.K_LSHIFT]:
                if keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d] or keys[pygame.K_w]:
                    if self.player.stamina.current_stamina >= 2:
                        self.player.hunger.hunger_timer += 2

            key_animation_map = {
                pygame.K_d: 1,  # Right animation
                pygame.K_a: 0,  # Left animation
                pygame.K_s: 3,  # Down animation
                pygame.K_w: 2  # Up animation
            }

            # initial animations
            for key, anim_index in key_animation_map.items():
                if keys[key]:
                    UniversalVariables.animation_index = anim_index
                    UniversalVariables.last_input = pygame.key.name(key)

            # combined animations
            if keys[pygame.K_s] or keys[pygame.K_w]:
                if keys[pygame.K_a]:
                    UniversalVariables.last_input += 'a'
                if keys[pygame.K_d]:
                    UniversalVariables.last_input += 'd'

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
                        self.frame = self.idle_swimming_animation_manager.update_animation(keys, is_idle)
                    else:
                        self.frame = self.swimming_animation_manager.update_animation(keys, is_idle)
                else:
                    if is_idle:
                        self.frame = self.idle_animation_manager.update_animation(keys, is_idle)
                    else:
                        self.frame = self.animation_manager.update_animation(keys, is_idle)

            else:
                pass
        except Exception as e: print(f'Error @ update.py: {e}')

    def get_player_rect(self):
        # Muudab playeri asukohta vastavalt kaamera asukohale / paiknemisele
        player_position_adjusted: tuple[int, int] = (UniversalVariables.player_x + UniversalVariables.offset_x,
                                                     UniversalVariables.player_y + UniversalVariables.offset_y)



        player_rect = pygame.Rect(player_position_adjusted[0] + UniversalVariables.player_hitbox_offset_x,
                                  player_position_adjusted[1] + UniversalVariables.player_hitbox_offset_y,
                                  UniversalVariables.player_width * 0.47, UniversalVariables.player_height * 0.74)

        self.player_rect = player_rect

        return player_rect



    def render_player(self) -> None:
        """ Renderib ainult playeri. """

        # Muudab playeri asukohta vastavalt kaamera asukohale / paiknemisele
        player_position_adjusted: tuple[int, int] = (UniversalVariables.player_x + UniversalVariables.offset_x, UniversalVariables.player_y + UniversalVariables.offset_y)

        blit_operations = [
            (self.frame, player_position_adjusted)
            # Add other blit operations here if they exist in the same rendering context.
        ]

        if not UniversalVariables.cutscene:
            UniversalVariables.screen.blits(blit_operations, doreturn=False)

        # Joonistab playeri ümber punase ringi ehk playeri hitboxi
        player_rect = pygame.Rect(player_position_adjusted[0] + UniversalVariables.player_hitbox_offset_x,
                                  player_position_adjusted[1] + UniversalVariables.player_hitbox_offset_y,
                                  UniversalVariables.player_width * 0.47, UniversalVariables.player_height * 0.74)
        self.player_rect = player_rect

        if not UniversalVariables.portal_list == []:
            x, y = int(UniversalVariables.portal_list[0][0]), int(UniversalVariables.portal_list[0][1])
            UniversalVariables.portal_frame_rect = pygame.Rect(x + UniversalVariables.offset_x,
                                                           y + UniversalVariables.offset_y,
                                                           UniversalVariables.block_size, UniversalVariables.block_size)

        # renderib playeri hitboxi
        if UniversalVariables.render_boxes_counter and UniversalVariables.debug_mode:
            pygame.draw.rect(UniversalVariables.screen, (255, 0, 0), self.player_rect, 2)

            if not UniversalVariables.portal_list == []:
                pygame.draw.rect(UniversalVariables.screen, "orange", UniversalVariables.portal_frame_rect, 2)

        UniversalVariables.player_width = UniversalVariables.player_width_factor * UniversalVariables.block_size
        UniversalVariables.player_height = UniversalVariables.player_height_factor * UniversalVariables.block_size


class EssentialsUpdate:
    def __init__(self, font, framerate):
        self.font = font
        self.framerate = framerate

        self.game_start_clock = (9, 0)
        self.time_update: int = 0
        self.game_day_count = 0
        self.day_night_text = 'Day'
        self.daylight_strength = 0

    # Function to calculate in-game time
    def calculate_time(self):
        day_night_text = self.day_night_text

        time = self.game_start_clock  # (9, 0)
        days = self.game_day_count
        hours = time[0]
        minutes = time[1]

        # Check if new minute should be added to game's time
        if UniversalVariables.game_minute_lenght <= self.time_update:
            minutes += 1
            self.time_update = 0

        # Update minutes -> hours, hours -> reset hours, minutes & add days
        if 60 <= minutes:
            hours += 1
            minutes = 0
        if 24 <= hours:
            hours = 0
            minutes = 0
            days += 1

        # Update variables
        self.time_update += 1
        self.game_day_count = days
        self.game_start_clock = (hours, minutes)

        # Update day, night text next to game_day_count

        if hours < 8 or hours >= 22:
            day_night_text = 'Night'
        else:
            day_night_text = 'Day'
        self.day_night_text = day_night_text

        if len(str(minutes)) == 1: minutes = f'0{minutes}'  # alati 2 nubrit minutite kohal
        return hours, minutes, days


    def calculate_daylight_strength(self):
        """ See func edastab self.daylight_strengthi vision draw_shadowile."""
        """ Draw_shadowis player_vision_conei valgustugevus self.daylight_strengthist """

        if not UniversalVariables.debug_mode:
            hours = self.game_start_clock[0]  # Get current time

            daylight_strength_map = {
                # range(kellaaeg, kellaaeg): value
                range(20, 21): 90,  # Evening (20 PM to 20:59 PM)
                range(21, 22): 125,
                range(22, 24): 175,
                range(0, 2): 235,
                range(2, 5): 215,
                range(5, 7): 180,
                range(7, 8): 110,
                range(8, 9): 100  # Dawn (8 AM to 8:59 AM)
            }

            self.daylight_strength = next(
                (strength for hour_range, strength in daylight_strength_map.items() if hours in hour_range),
                100  # Default value
            )

    def render_gui_text(self, text, position, color=(100, 255, 100), debug=None):
        """Utility function to render text on the screen."""
        if not debug:
            text_surface = self.font.render(text, True, color)
            UniversalVariables.text_sequence.append((text_surface, position))
        if UniversalVariables.debug_mode:
            text_surface = self.font.render(text, True, color)
            UniversalVariables.text_sequence.append((text_surface, position))


    def render_general(self):
        fps_text = 'FPS unlocked'
        if UniversalVariables.fps_lock: fps_text = 'FPS locked'

        ui_elements = [
            (f"{self.framerate.display_fps_statistics()}", (5, 5)),  # FPS display
            (f"Time {EssentialsUpdate.calculate_time(self)[0]}:{EssentialsUpdate.calculate_time(self)[1]}", (5, 35)),
            (f"{self.day_night_text} {EssentialsUpdate.calculate_time(self)[2]}", (5, 65)),

            ("H - Show hitboxes", (UniversalVariables.screen_x / 2, 5), "YELLOW", True),
            ("J - Switch light", (UniversalVariables.screen_x / 2, 35), "YELLOW", True),
            (f"G - {fps_text}", (UniversalVariables.screen_x / 2, 65), "YELLOW", True)

        ]
        for element in ui_elements:
            text = element[0]
            position = element[1] if len(element) > 1 else None
            color = element[2] if len(element) > 2 else (100, 255, 100)  # Default color white if not specified
            if len(element) == 4:
                debug_mode = element[3]

            # Call the improved render_text function with the specified parameters
                self.render_gui_text(text, position=position, color=color, debug=debug_mode)
            else:
                self.render_gui_text(text, position=position, color=color)


class Framerate:
    def __init__(self):
        # self.universal = universal
        ...

    def get_fps_statistics(self):
        if not UniversalVariables.fps_list:
            return 0.0, 0.0, 0.0

        avg_fps = sum(UniversalVariables.fps_list) / len(UniversalVariables.fps_list)
        min_fps = min(UniversalVariables.fps_list)
        max_fps = max(UniversalVariables.fps_list)
        return int(avg_fps), int(min_fps), int(max_fps)


    def display_fps_statistics(self):
        avg_fps, min_fps, max_fps = self.get_fps_statistics()
        try:  current_fps = int(UniversalVariables.fps_list[-1])
        except IndexError: current_fps = 0
        fps_text = f"FPS {current_fps} [Avg: {avg_fps}, Min: {min_fps}, Max: {max_fps}]"  # avg, min, max, last value of the fps num list >:)
        return fps_text
