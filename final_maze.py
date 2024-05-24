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

            pygame.display.flip()

    def change_ground(self) -> None:
        """Muudab groundi None'iks"""
        original_x, original_y = find_number_in_list_of_lists(self.terrain_data, 1000)

        # Muudab iga 20 ticki tagant groundi
        if Final_Maze.delay == 20:

            x_0 = original_x - RenderPictures.render_range * 2 - 2 + Final_Maze.x_00
            y_0 = original_y - RenderPictures.render_range * 2 - 2 + Final_Maze.y_00
            x_1 = original_x + RenderPictures.render_range * 2 + 3 + Final_Maze.x_11
            y_1 = original_y + RenderPictures.render_range * 2 + 3 + Final_Maze.y_11

            for x in range(original_x - RenderPictures.render_range * 2,
                           original_x + RenderPictures.render_range * 2 + 3):
                self.terrain_data[x][y_0] = None
                self.terrain_data[x][y_1] = None

            for y in range(original_y - RenderPictures.render_range * 2,
                           original_y + RenderPictures.render_range * 2 + 3):
                self.terrain_data[x_0][y] = None
                self.terrain_data[x_1][y] = None

            # Resetib uue rea jaoks x ja y
            Final_Maze.x_00 += 1
            Final_Maze.y_00 += 1
            Final_Maze.x_11 -= 1
            Final_Maze.y_11 -= 1

            Final_Maze.delay = 0

        # Vaatab kuna peab cutscene'ist välja tulema
        if abs(Final_Maze.y_11) == 9:
            UniversalVariables.cutscene = False

    def final_maze_update(self) -> None:
        """Update final maze state."""
        Final_Maze.handle_portal_interaction(self)
        if UniversalVariables.cutscene:
            Final_Maze.change_ground(self)
