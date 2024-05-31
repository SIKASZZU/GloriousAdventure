import pygame

from variables import UniversalVariables
from collisions import find_number_in_list_of_lists
from render import RenderPictures


class Final_Maze:
    delay: int = 0
    y_00: int = 0
    y_11: int = 0
    x_00: int = 0
    x_11: int = 0

    def handle_portal_interaction(self) -> None:
        """Kui player läheb portali sisse siis ta detectib selle ära ja ei lase enam playeril liikuda + hide player"""

        # Resetib delay kui player pole portalisse läinud
        if not UniversalVariables.cutscene:
            Final_Maze.delay = 0

        # Vaatab kas player läks portalisse või mitte
        if UniversalVariables.portal_frame_rect:
            if UniversalVariables.portal_frame_rect.colliderect(self.player_rect):
                UniversalVariables.cutscene = True
                UniversalVariables.portal_frame_rect = None
                UniversalVariables.portal_list = []

    def change_ground(self) -> None:
        """Muudab groundi None'iks"""
        
        original_x, original_y = find_number_in_list_of_lists(self.terrain_data, 1000)
        
        UniversalVariables.ui_elements.append("""   Thanks for playing.   """)

        # Muudab iga 20 ticki tagant groundi
        if Final_Maze.delay == 20:

            x_0 = original_x - RenderPictures.render_range * 2 - 2 + Final_Maze.x_00
            y_0 = original_y - RenderPictures.render_range * 2 - 2 + Final_Maze.y_00
            x_1 = original_x + RenderPictures.render_range * 2 + 3 + Final_Maze.x_11
            y_1 = original_y + RenderPictures.render_range * 2 + 3 + Final_Maze.y_11

            for x in range(original_x - RenderPictures.render_range * 2,
                           original_x + RenderPictures.render_range * 2 + 3):
                self.terrain_data[x][y_0] = 999
                self.terrain_data[x][y_1] = 999

            for y in range(original_y - RenderPictures.render_range * 2,
                           original_y + RenderPictures.render_range * 2 + 3):
                self.terrain_data[x_0][y] = 999
                self.terrain_data[x_1][y] = 999

            # Resetib uue rea jaoks x ja y
            Final_Maze.x_00 += 1
            Final_Maze.y_00 += 1
            Final_Maze.x_11 -= 1
            Final_Maze.y_11 -= 1

            Final_Maze.delay = 0

            # Vaatab kuna peab cutscene'ist välja tulema
            if abs(Final_Maze.y_11) == 10:

                # UniversalVariables.player_x = UniversalVariables.block_size * 40.75  # Teleb final bossi mapi keskele
                # UniversalVariables.player_y = UniversalVariables.block_size * 40.75  # Teleb final bossi mapi keskele
                # self.terrain_data = Final_Maze.generate_map_with_portal(80)  # See teeb final boss mapi
                # Create a black surface

                UniversalVariables.cutscene = False
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

    def final_maze_update(self) -> None:
        """Update final maze state."""
        Final_Maze.handle_portal_interaction(self)
        if UniversalVariables.cutscene:
            Final_Maze.change_ground(self)
