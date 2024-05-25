import pygame
import sys
import textwrap

# Pythoni inbuilt/downloaded files
from components import Player, StaminaComponent

# Oma enda failid
from entity import Enemy
from variables import UniversalVariables
from camera import Camera  # box_target_camera
from render import RenderPictures  # map_render
from mbd import event_mousebuttondown
from map import MapData  # glade_creation, map_list_to_map
from objects import ObjectManagement  # place_and_render_object
from render import CreateCollisionBoxes  # object_list_creation
import vision  # find_boxes_in_window, draw_light_source_and_rays
from menu import Menu, PauseMenu  # main_menu, PauseMenu: settings_menu
from update import EssentialsUpdate  # check_pressed_keys, render_general
from update import PlayerUpdate  # update_player, render_player, render_HUD
from inventory import Inventory  # handle_mouse_click, render_craftable_items
from collisions import Collisions, reset_clicks  # check_collisions, collision_terrain, collision_hitbox
from audio import Player_audio  # player_audio_update
from loot import Loot  # loot_update
from blade import change_blades
from final_maze import Final_Maze
from components import HungerComponent
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Glorious Adventure - BETA")
        self.clock = pygame.time.Clock()  # FPS
        self.font = pygame.font.SysFont("Verdana", 20)  # Font

        self.player = Player(max_health=20, min_health=0, max_stamina=20, min_stamina=0, base_speed=4, max_speed=10, min_speed=1, base_hunger=20, max_hunger=20, min_hunger=0)
        self.player_rect = None  # Player rect to be set in the game

        self.screen = UniversalVariables.screen
        self.game_menu_state = "main"
        self.pause_menu_state = "main"

        self.daylight_strength = 0
        self.dim_surface = pygame.Surface((UniversalVariables.screen_x, UniversalVariables.screen_y), pygame.SRCALPHA, 32)

        self.print_hp = 0
        self.restrict_looping = False

        self.terrain_data = None
        self.click_position = ()
        self.click_window_x = None
        self.click_window_y = None

        glade_data = MapData.glade_creation()
        if not self.terrain_data:
            self.terrain_data = MapData.map_list_to_map(self)

        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                if self.terrain_data[i][j] == 933:
                    self.terrain_data[i - 1][j] = 98

        self.font = pygame.font.SysFont(None, 30)

        # UniversalVariables.ui_elements.append(
        #     "Your persistence pays off as you discover a hidden chamber."
        #     "Glittering treasures and powerful artifacts are yours for the taking, but beware"
        #     "such riches are often fiercely guarded."
        # )

        self.shown_texts = set()
        self.text_fade_duration = 700  # Duration of each fade in milliseconds
        self.text_elements = []  # Store text elements with their fade state

    def event_game_state(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def events(self):
        for event in pygame.event.get():
            self.event_game_state(event)
            event_mousebuttondown(self, event)

    def load_variables(self):
        UniversalVariables()

    def render_general(self):
        for text in UniversalVariables.ui_elements:
            if text not in self.shown_texts:
                self.add_fading_text(text)
                self.shown_texts.add(text)

    def add_fading_text(self, text, color=(255, 255, 255), background_color=(30, 30, 30), padding=5):
        """Add text with a background to be rendered with a fading effect."""
        max_width = UniversalVariables.screen_x  # Max width with padding

        # Start with a relatively large font size
        font_size = 20
        font = pygame.font.SysFont("Verdana", font_size)
        lines = textwrap.wrap(text, width=max_width // font_size)

        # Decrease font size until the text fits within the screen bounds
        while True:
            text_surfaces = []
            text_rects = []

            for line in lines:
                text_surface = font.render(line, True, color)
                text_rect = text_surface.get_rect()
                text_surfaces.append(text_surface)
                text_rects.append(text_rect)

            total_height = sum(rect.height for rect in text_rects) + (len(text_rects) - 1) * padding
            if total_height < UniversalVariables.screen_y * 0.9:
                break
            else:
                font_size -= 1
                font = pygame.font.SysFont("Verdana", font_size)
                lines = textwrap.wrap(text, width=max_width // font_size)

        # Position the text so that its bottom aligns with UniversalVariables.screen_y * 0.9
        start_y = UniversalVariables.screen_y * 0.9 - total_height

        # Calculate the total width and height for the background surface
        max_text_width = max(text_rect.width for text_rect in text_rects)
        background_surface = pygame.Surface((max_text_width + 2 * padding, total_height + 2 * padding), pygame.SRCALPHA)
        pygame.draw.rect(background_surface, background_color, background_surface.get_rect(), border_radius=20)
        background_surface.set_alpha(100)  # Set transparency to 100

        # Center the background surface on the screen
        background_rect = background_surface.get_rect(
            center=(UniversalVariables.screen_x // 2, start_y + total_height // 2))

        # Center text lines within the background surface
        current_y = padding
        for text_surface, text_rect in zip(text_surfaces, text_rects):
            text_rect.topleft = (padding, current_y)
            current_y += text_rect.height + padding

        # Create a list of tuples with the background surface, its rect, and the text surfaces with their rects
        start_time = pygame.time.get_ticks()
        duration = len(text) * 0.05 * 1000  # Duration based on text length

        # Remove the currently displayed text element, if any
        self.text_elements = []

        self.text_elements.append(
            (background_surface, background_rect, text_surfaces, text_rects, start_time, True, duration))

    def handle_fading_texts(self):
        """Handle the fading effect for all text elements."""
        current_time = pygame.time.get_ticks()
        new_text_elements = []
        for background_surface, background_rect, text_surfaces, text_rects, start_time, fade_in, duration in self.text_elements:
            elapsed_time = current_time - start_time
            if fade_in:
                if elapsed_time < 500:  # Fade in for 0.5 seconds
                    alpha = (elapsed_time / 500) * 255
                elif elapsed_time < duration + 500:  # Stay at full opacity for text length * 0.05 seconds
                    alpha = 255
                elif elapsed_time < duration + 1000:  # Fade out for 0.5 seconds
                    alpha = 255 - ((elapsed_time - (duration + 500)) / 500) * 255
                else:
                    continue  # Fade out complete, do not re-add to new_text_elements

                # Blit the background once
                background_surface.set_alpha(min(alpha, 100))  # Limit alpha to 100
                self.screen.blit(background_surface, background_rect)

                # Blit each line of text
                for text_surface, text_rect in zip(text_surfaces, text_rects):
                    text_surface.set_alpha(min(alpha, 255))  # Limit alpha to 255 for text
                    centered_text_rect = text_rect.copy()
                    centered_text_rect.centerx = background_rect.centerx
                    centered_text_rect.top = background_rect.top + text_rect.top
                    self.screen.blit(text_surface, centered_text_rect.topleft)

                new_text_elements.append(
                    (background_surface, background_rect, text_surfaces, text_rects, start_time, True, duration))
            else:
                if elapsed_time < 500:  # Fade out for 0.5 seconds
                    alpha = 255 - (elapsed_time / 500) * 255
                else:
                    continue  # Fade out complete, do not re-add to new_text_elements

                # Blit the background once
                background_surface.set_alpha(min(alpha, 100))  # Limit alpha to 100
                self.screen.blit(background_surface, background_rect)

                # Blit each line of text
                for text_surface, text_rect in zip(text_surfaces, text_rects):
                    text_surface.set_alpha(min(alpha, 255))  # Limit alpha to 255 for text
                    centered_text_rect = text_rect.copy()
                    centered_text_rect.centerx = background_rect.centerx
                    centered_text_rect.top = background_rect.top + text_rect.top
                    self.screen.blit(text_surface, centered_text_rect.topleft)

                new_text_elements.append(
                    (background_surface, background_rect, text_surfaces, text_rects, start_time, False, duration))

        self.text_elements = new_text_elements

    def call_technical(self):
        PlayerUpdate.update_player(self)  # Update player position and attributes
        Camera.box_target_camera(self)  # Camera follow

        Collisions.collison_terrain(self)
        Collisions.check_collisions(self)  # Check player collisions

        CreateCollisionBoxes.object_list_creation(self)  # Create collision boxes
        vision.find_boxes_in_window()

        self.player.health.check_health()
        Enemy.update(self)
        Player_audio.player_audio_update(self)
        change_blades(self)

    def call_visuals(self):
        RenderPictures.map_render(self)  # Render terrain
        if Collisions.render_after:
            ObjectManagement.place_and_render_object(self)  # Render objects
            PlayerUpdate.render_player(self)  # Render player
        else:
            PlayerUpdate.render_player(self)
            ObjectManagement.place_and_render_object(self)

        Enemy.spawn(self)
        EssentialsUpdate.calculate_daylight_strength(self)
        vision.draw_light_source_and_rays(self, UniversalVariables.screen, self.player_rect.center, UniversalVariables.light_range)
        PlayerUpdate.render_HUD(self)  # Render HUD
        EssentialsUpdate.render_general(self)  # Render other elements

        # Equipped item slot
        if UniversalVariables.equipped_item:
            item = UniversalVariables.equipped_item
            Inventory.render_inventory_slot(self, item)
        else:
            item = None
            Inventory.render_inventory_slot(self, item)

    def check_keys(self):
        EssentialsUpdate.check_pressed_keys(self)  # Check pressed keys

    def reset_lists(self):
        UniversalVariables.text_sequence = []
        UniversalVariables.blits_sequence = []

    def refresh_loop(self):
        Collisions.keylock = 0
        self.screen.blits(UniversalVariables.text_sequence)
        pygame.display.update()
        self.clock.tick(UniversalVariables.FPS)

    def printing(self):
        Inventory.print_inventory()
        Camera.print_clicks(self)
        self.player.health.print_health()

    def custom_addition(self):
        if UniversalVariables.debug_mode == True:
            if not self.restrict_looping:
                ObjectManagement.add_object_from_inv("Maze_Key", 100)
                self.restrict_looping = True

    def run(self):
        self.load_variables()
        while True:
            self.events()

            self.reset_lists()
            self.call_technical()
            self.call_visuals()

            Inventory.call_inventory(self)
            if Inventory.render_inv: Inventory.render_inventory(self)  # Render inventory

            Final_Maze.final_maze_update(self)
            self.render_general()
            self.handle_fading_texts()  # Render fading text after everything else

            self.refresh_loop()

            # ******************** DEBUG MODE ******************** #
            if UniversalVariables.debug_mode:
                UniversalVariables.ui_elements.append("!        Debug mode - True        !")
                self.player.speed.base_speed = 20
                
                # neil functionitel on juba sees, et kontrolliks debug modei
                self.check_keys()
                self.custom_addition()
            # UniversalVariables.player_x, UniversalVariables.player_y = 2500, 6000   # FPS'side testimiseks

            Final_Maze.delay += 1


if __name__ == "__main__":
    game = Game()
    game.run()
