import pygame
import random
from variables import UniversalVariables


class MazeGenerator:
    def __init__(self, width, height, cell_size):
        self.WIDTH = width
        self.HEIGHT = height
        self.CELL_SIZE = cell_size
        self.GRID_WIDTH = self.WIDTH // self.CELL_SIZE
        self.GRID_HEIGHT = self.HEIGHT // self.CELL_SIZE

        # Colors
        self.WHITE = (50, 50, 50)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        # Initialize Pygame
        pygame.init()
        UniversalVariables.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Maze Generator")

        # Create a grid
        self.grid = [[1 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]

        # Generate the maze
        self.generate_maze()

        # Set starting and finishing points
        self.start_x, self.start_y = 1, 1
        self.finish_x, self.finish_y = self.GRID_WIDTH - 2, self.GRID_HEIGHT - 2

    def generate_maze(self):
        self._recursive_backtracking(0, 0)

    def _recursive_backtracking(self, x, y):
        self.grid[y][x] = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + 2 * dx, y + 2 * dy
            if 0 <= new_x < self.GRID_WIDTH and 0 <= new_y < self.GRID_HEIGHT and self.grid[new_y][new_x]:
                self.grid[y + dy][x + dx] = 0
                self._recursive_backtracking(new_x, new_y)

    def draw_maze(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            UniversalVariables.screen.fill(self.WHITE)

            for y in range(self.GRID_HEIGHT):
                for x in range(self.GRID_WIDTH):
                    if self.grid[y][x]:
                        pygame.draw.rect(UniversalVariables.screen, self.BLACK,
                                         (x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

            # Draw the starting point (red dot)
            pygame.draw.circle(UniversalVariables.screen, self.RED, (
                self.start_x * self.CELL_SIZE + self.CELL_SIZE // 2,
                self.start_y * self.CELL_SIZE + self.CELL_SIZE // 2),
                               self.CELL_SIZE // 3)

            # Draw the finishing point (green dot)
            pygame.draw.circle(UniversalVariables.screen, self.GREEN, (
                self.finish_x * self.CELL_SIZE + self.CELL_SIZE // 2,
                self.finish_y * self.CELL_SIZE + self.CELL_SIZE // 2),
                               self.CELL_SIZE // 3)

            pygame.display.flip()

        # Quit Pygame
        pygame.quit()


if __name__ == "__main__":
    maze = MazeGenerator(1920, 1080, 40)
    maze.draw_maze()
