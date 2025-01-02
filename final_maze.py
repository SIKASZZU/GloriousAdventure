import pygame

from functions import UniversalFunctions


class Final_Maze:
    def __init__(self, terrain_data, tile_sounds, render, variables):
        self.terrain_data = terrain_data
        self.tile_sounds = tile_sounds
        self.render = render
        self.variables = variables

        self.delay: int = 0
        self.y_00: int = 0
        self.y_11: int = 0
        self.x_00: int = 0
        self.x_11: int = 0

    def handle_portal_interaction(self) -> None:
        """Kui player läheb portali sisse siis ta detectib selle ära ja ei lase enam playeril liikuda + hide player"""

        # Resetib delay kui player pole portalisse läinud
        if not self.variables.cutscene:
            self.delay = 0

        # Vaatab kas player läks portalisse või mitte
        if self.variables.portal_frame_rect:
            if self.variables.portal_frame_rect.colliderect(self.player_rect):
                self.variables.cutscene = True
                self.variables.portal_frame_rect = None
                self.variables.portal_list = []

    def change_ground(self) -> None:
        """Muudab groundi None'iks"""
        
        original_x, original_y = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 1000)
        
        self.variables.ui_elements.append("""   Thanks for playing.   """)

        # Muudab iga 20 ticki tagant groundi
        if self.delay == 20:

            x_0 = original_x - self.render.render_range * 2 - 2 + self.x_00
            y_0 = original_y - self.render.render_range * 2 - 2 + self.y_00
            x_1 = original_x + self.render.render_range * 2 + 3 + self.x_11
            y_1 = original_y + self.render.render_range * 2 + 3 + self.y_11

            for x in range(original_x - self.render.render_range * 2,
                           original_x + self.render.render_range * 2 + 3):
                self.terrain_data[x][y_0] = 999
                self.terrain_data[x][y_1] = 999

            for y in range(original_y - self.render.render_range * 2,
                           original_y + self.render.render_range * 2 + 3):
                self.terrain_data[x_0][y] = 999
                self.terrain_data[x_1][y] = 999

            # Resetib uue rea jaoks x ja y
            self.x_00 += 1
            self.y_00 += 1
            self.x_11 -= 1
            self.y_11 -= 1

            self.delay = 0

            # Vaatab kuna peab cutscene'ist välja tulema
            if abs(self.y_11) == 10:

                # self.variables.player_x = self.variables.block_size * 40.75  # Teleb final bossi mapi keskele
                # self.variables.player_y = self.variables.block_size * 40.75  # Teleb final bossi mapi keskele
                # self.terrain_data = self.generate_map_with_portal(80)  # See teeb final boss mapi
                # Create a black surface

                self.variables.cutscene = False
                pygame.quit()

    def generate_map_with_portal(size=80):
        import random
        # Initialize the map with all 99s
        map_grid = [[99 for _ in range(size)] for _ in range(size)]

        # Fill the inside with 80% 99 and 20% 98
        for i in range(1, size - 1):
            for j in range(1, size - 1):
                if random.random() < 0.9:
                    map_grid[i][j] = 98
                elif random.random() < 0.007:
                    map_grid[i][j] = 1001
                else:
                    map_grid[i][j] = 99

        # Place a 1x1 portal (value 1000) in the middle of the map
        middle = size // 2
        map_grid[middle][middle] = 1000

        # Place five 98 blocks next to the portal
        adjacent_positions = [
            (middle - 1, middle),  # Above
            (middle + 1, middle),  # Below
            (middle, middle - 1),  # Left
            (middle, middle + 1),  # Right
            (middle - 1, middle - 1),  # Top-left diagonal
        ]

        for pos in adjacent_positions:
            map_grid[pos[0]][pos[1]] = 98

        return map_grid

    def portal(self):

        if self.variables.final_maze == False:
            return
        if self.variables.portal_frames > 0:
            _ = self.variables.portal_frames
            for i in range(_):
                UniversalFunctions.gray_yellow(self, 'yellow')
                self.variables.portal_frames -= 1

                if i == 7:
                    self.variables.portal_frames = 0
                    break

        # Teeb portali valmis
        if not UniversalFunctions.count_occurrences_in_list_of_lists(self.terrain_data, 982) >= 8:
            return
        if UniversalFunctions.count_occurrences_in_list_of_lists(self.terrain_data, 555):
            return

        else:
            text = (
                    "As the final key slides into place, the portal shimmers open, "
                    "revealing its arcane depths. A resounding hum fills the air, "
                    "echoing through the labyrinth as the portal's magic pulses with newfound life."
                )
            if text not in self.fading_text.shown_texts:
                self.variables.ui_elements.append(text)

            self.variables.portal_list = []
            self.tile_sounds.portal_open_audio()
            UniversalFunctions.yellow_green(self, 'green')
            x, y = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 555)
            self.terrain_data[x+1][y] = 1000
            portal_y, portal_x =\
                ((x+1) * self.variables.block_size) + self.variables.block_size / 2,\
                (y * self.variables.block_size) + self.variables.block_size / 2

            self.variables.portal_list.append((portal_x, portal_y))

    def update(self) -> None:
        """Update final maze state."""
        
        self.handle_portal_interaction()
        if self.variables.cutscene:
            self.change_ground()

        self.portal()