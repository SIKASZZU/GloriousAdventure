import os
import sys
import numpy as np
from skimage.transform import resize
from collections import deque
import random

from variables import UniversalVariables
from variables import GameConfig


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MapData:
    def __init__(self, terrain_data, click_position, camera):
        # Initilazitud asjad
        self.click_position = click_position
        self.terrain_data = terrain_data
        self.camera = camera

        # MapData asjad
        self.placeholder = [[None] * 40 for _ in range(40)]
        self.maze_size = 40
        self.resolution = (self.maze_size, self.maze_size)  # Adjusted resolution of Perlin noise for more distributed walls

        self.create_save_puzzle = None
        self.converted_maze = []

        if UniversalVariables.debug_mode:
            self._puzzle_pieces = 20
            self._keyholders = 20
            self._loot = 20
        else:
            self._puzzle_pieces = 6  # on vaja kindlasti rohkem, kui kaheksa
            self._keyholders = 4     # on vaja kaheksa
            self._loot = random.randint(3, 5)  # _loot = random.randint(3, 5)


    def create_start_doors(self, maze, start_side):
        """ Creates start door using cursor grid data. """
        """ Selle funciga saab random exit doori asemele starteri panna. """

        door_tuple = self.camera.left_click_on_screen(self.camera.click_position)
        door_grid_map = self.camera.click_on_screen_to_grid(door_tuple[0], door_tuple[1])

        if None in door_grid_map and UniversalVariables.maze_counter <= 1:
            door_grid = (self.maze_size // 2 - 1, self.maze_size // 2 - 1)

        else:
            door_grid = (door_grid_map[0] % 39, door_grid_map[1] % 39)  # kuna siin on 40x40 ala ss door grid arvutatakse just 40x40 ala sisse

        # Kui player vajutab parempoolsele uksele, ss addition fixib selle, et uue ukse location jaaks samaks!
        addition = self.check_for_door(start_side, door_grid_map)
        if addition == None:  addition = 1

        # Set the start point
        if start_side == 'left':
            start_0 = (door_grid[0], 0)
            start_1 = (door_grid[0] + addition, 0)
            maze[start_0] = 90 
            maze[start_1] = 90

        elif start_side == 'top':
            start_0 = (0, door_grid[1])
            start_1 = (0, door_grid[1] + addition)
            maze[start_0] = 91 
            maze[start_1] = 91

        elif start_side == 'right':
            start_0 = (door_grid[0], self.maze_size - 1)
            start_1 = (door_grid[0] + addition, self.maze_size - 1)
            maze[start_0] = 92 
            maze[start_1] = 92

        elif start_side == 'bottom':
            start_0 = (self.maze_size - 1, door_grid[1])
            start_1 = (self.maze_size - 1, door_grid[1] + addition)
            maze[start_0] = 93 
            maze[start_1] = 93

        return maze, (start_0, start_1)


    def check_for_door(self, start_from, door_grid_map):
        if None in door_grid_map:
            return None
        
        xxx = self.terrain_data[door_grid_map[0]][door_grid_map[1] - 1]
        yyy = self.terrain_data[door_grid_map[0] - 1][door_grid_map[1]]        
        
        if start_from == 'right' or start_from == 'left':
            if yyy in GameConfig.CLOSED_DOOR_IDS.value:
                return -1
            
        elif start_from == 'top' or start_from == 'bottom':
            if xxx in GameConfig.CLOSED_DOOR_IDS.value:
                return -1
        
        return None

    def create_maze_items(self, maze):

        def spawn_key(maze, x, y):
            rand_val = random.random()
            if rand_val < 0.1:
                maze[x][y] = 10  # 10% full key
            elif rand_val < 0.6:
                maze[x][y] = 12  # 50% key top half
            else:
                maze[x][y] = 13  # 50% key bottom half


        def place_item(maze, item_value, count):
            for _ in range(count):
                while True:
                    x, y = random.randint(3, self.maze_size - 4), random.randint(3, self.maze_size - 4)
                    if maze[x][y] == 99 and not self.is_dead_end(maze, x, y):
                        print(x, y, type(x), type(y))
                        if item_value == 'keys':  
                            spawn_key(maze, x, y)
                        else: 
                            maze[x][y] = item_value                        
                        break

        # Place maze keys
        place_item(maze, 'keys', self._puzzle_pieces)

        # Place maze puzzle pieces
        # place_item(maze, None, self._puzzle_pieces)  # mingi solutioni placeholder!!!!

        # Place maze keyholders
        place_item(maze, 981, self._keyholders)

        # Place maze loot barrels
        place_item(maze, 1001, self._loot)

        return maze
    
    def is_dead_end(self, maze, x, y):
        walls = 0
        if maze[x-1][y] == 99:
            walls += 1
        if maze[x+1][y] == 99:
            walls += 1
        if maze[x][y-1] == 99:
            walls += 1
        if maze[x][y+1] == 99:
            walls += 1
        return walls >= 3  # kui on 3 v6i rohkem ss on True ja pekkis

    @staticmethod
    def block_maze_noise(shape, res):
        def f(t):
            # return 1*t**7 - 5*t**0 + 1*t**1
            return 1*t**7 - 5*t**0 + 1*t**1

        grid = np.mgrid[0:res[0],0:res[1]].transpose(1, 2, 0)
        grid = grid / res

        gradients = np.random.rand(res[0] + 1, res[1] + 1, 2)
        gradients /= np.linalg.norm(gradients, axis=2, keepdims=True)

        g00 = gradients[:-1,:-1]
        g10 = gradients[1:,:-1]
        g01 = gradients[:-1,1:]
        g11 = gradients[1:,1:]

        t = grid - grid.astype(int)
        fade_t = f(t)

        n00 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1])) * g00, axis=2)
        n10 = np.sum(np.dstack((grid[:,:,0] - 1, grid[:,:,1])) * g10, axis=2)
        n01 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1] - 1)) * g01, axis=2)
        n11 = np.sum(np.dstack((grid[:,:,0] - 1, grid[:,:,1] - 1)) * g11, axis=2)

        n0 = n00 * (1 - fade_t[:,:,0]) + n10 * fade_t[:,:,0]
        n1 = n01 * (1 - fade_t[:,:,0]) + n11 * fade_t[:,:,0]

        noise = np.sqrt(2) * (n0 * (1 - fade_t[:,:,1]) + n1 * fade_t[:,:,1])
        return noise

    @staticmethod
    def is_valid(x, y, maze):
        return 0 <= x < len(maze) and 0 <= y < len(maze[x]) and maze[x][y] != 99
    
    def find_path_bfs(self, maze, start, end):
        queue = deque([(start, [])])
        visited = set()
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == end:
                return path

            if (x, y) not in visited:
                visited.add((x, y))
                for dx, dy in directions:
                    new_x, new_y = x + dx, y + dy
                    if self.is_valid(new_x, new_y, maze):
                        new_path = path + [(new_x, new_y)]
                        queue.append(((new_x, new_y), new_path))

        return None


    def search_paths(self, maze, type_of_maze, start_side, start_door_grid, exit_point=None):
        """ maze is list numpy.ndarray . type_of_maze is block_maze, labyrinth_maze, final_maze, blade_maze etc. """

        if exit_point != None:
            end_positions = [
                (exit_point[0]), (exit_point[1])
            ]
            
        else:
            end_positions = [
                (19, 38), (20, 38),
                (1, 19), (1, 20),
                (19, 1), (20, 1),
                (38, 19), (38, 20)
            ]
            
        special_positions = []
        start_positions = [start_door_grid[0], start_door_grid[1]]  # y, x
        # Check paths from each start to each end and special positions
        for start in start_positions:
            for end in end_positions + special_positions:
                path = self.find_path_bfs(maze, start, end)
                if path is None:
                    print(f"No path found from {start} to {end}")
                    self.create_save_puzzle = False

                else:
                    self.create_save_puzzle = True
                    
                    # check visually, kas path on valid v6i mitte.
                    # for tuple in path:
                    #     maze[tuple[0]][tuple[1]] = 2
        
        if self.create_save_puzzle == False:
            if type_of_maze == 'block_maze':
                maze = self.block_maze_generation(start_side)
                
            elif type_of_maze == 'labyrinth_maze':
                maze = self.labyrinth_maze_generation(start_side)
            self.search_paths(maze, type_of_maze, start_side, start_door_grid, exit_point)

    @staticmethod
    def buffer_doors(maze, first_door=None, second_door=None, start_side=None):
        if first_door[0] % 39 == 0 and start_side == 'bottom':
            maze[first_door[0] - 2, first_door[1]    ] = 2
            maze[first_door[0] - 1, first_door[1]    ] = 2
            maze[first_door[0] - 2, second_door[1]   ] = 2
            maze[first_door[0] - 1, second_door[1]   ] = 2

        elif first_door[0] % 39 == 0 and start_side == 'top':
            maze[first_door[0] + 2, first_door[1]    ] = 2
            maze[first_door[0] + 1, first_door[1]    ] = 2
            maze[first_door[0] + 2, second_door[1]   ] = 2
            maze[first_door[0] + 1, second_door[1]   ] = 2


        elif first_door[1] % 39 == 0 and start_side == 'right':
            maze[first_door[0]     , first_door[1] - 2] = 2
            maze[first_door[0]     , first_door[1] - 1] = 2
            maze[second_door[0]    , first_door[1] - 2] = 2
            maze[second_door[0]    , first_door[1] - 1] = 2

        elif first_door[1] % 39 == 0 and start_side == 'left':
            maze[first_door[0]     , first_door[1] + 2] = 2
            maze[first_door[0]     , first_door[1] + 1] = 2
            maze[second_door[0]    , first_door[1] + 2] = 2
            maze[second_door[0]    , first_door[1] + 1] = 2


    ### SIIT ALGAB MAZEIDE LOOMISE FUNCID  ###
    @staticmethod
    def glade_creation():
        glade_file_path = resource_path('glade.txt')
        with open(glade_file_path, 'r') as file:
            return [[int(x) for x in line.strip().replace('[', '').replace(']', '').split(',') if x.strip()]
                    for line in file if line.strip()]


    def file_to_maze(self, file_name: str, side: str = None):
        if side is None:
            maze_file_path = resource_path('glade.txt')
        else:
            maze_file_path = resource_path(file_name)

        maze = []
        with open(maze_file_path, 'r') as file:
            maze = [[int(x) if x.strip().lower() != 'none' else None
                     for x in line.strip().replace('[', '').replace(']', '').split(',') if x.strip()]
                    for line in file if line.strip()]
        self.maze_size = len(maze)
        maze = np.array(maze, dtype=object)  # Use dtype=object to handle None values # Teeb listi -> numpy arrayks.

        maze, start_door_grid = self.create_start_doors(maze, side)
        # compiler bitching
        if side == None:
            pass
        else:
            sides = ['top', 'bottom', 'left', 'right']
            sides.remove(side)
            for side in sides:

                if side == 'left':
                    end_0 = ((self.maze_size // 2), 0)
                    end_1 = ((self.maze_size // 2) - 1, 0)
                    maze[end_0[0]][end_0[1]], maze[end_1[0]][end_1[1]] = 94, 94

                elif side == 'top':
                    end_0 = (0, (self.maze_size // 2))
                    end_1 = (0, (self.maze_size // 2) - 1)
                    maze[end_0[0]][end_0[1]], maze[end_1[0]][end_1[1]] = 95, 95

                elif side == 'right':
                    end_0 = ((self.maze_size // 2), self.maze_size - 1)
                    end_1 = ((self.maze_size // 2) - 1, self.maze_size - 1)
                    maze[end_0[0]][end_0[1]], maze[end_1[0]][end_1[1]] = 96, 96

                elif side == 'bottom':
                    end_0 = (self.maze_size - 1, (self.maze_size // 2))
                    end_1 = (self.maze_size - 1, (self.maze_size // 2) - 1)
                    maze[end_0[0]][end_0[1]], maze[end_1[0]][end_1[1]] = 97, 97

            return maze


    def final_maze_generation(self, start_side):
        UniversalVariables.final_maze = True
        return self.file_to_maze(file_name='final_maze.txt', side=start_side)


    def blade_maze_generation(self, start_side):
        UniversalVariables.blades_spawned = True
        return self.file_to_maze(file_name='blade_maze.txt', side=start_side)

    def abandoned_glade_generation(self, start_side):
        type_maze = 'abandoned_glade'
        import noise

        def generate_glade_terrain(width, height, scale=0.1):
            terrain = []
            seed = random.randint(0, 1000)  # Random seed for different terrain each time

            for y in range(height):
                row = []
                for x in range(width):
                    value = noise.pnoise2(x * scale + seed * 0.46, y * scale + seed * 0.46, octaves=10)
                    row.append(value)
                terrain.append(row)
            return terrain

        def render(noise):
            abandoned_glade_maze = []

            for y, row in enumerate(noise):
                glade_row = []
                for x, value in enumerate(row):
                    terrain_value = 0 if value < -0.03 else 1
                    glade_row.append(terrain_value)

                abandoned_glade_maze.append(glade_row)
            return abandoned_glade_maze

        self.maze_size = self.maze_size
        noise = generate_glade_terrain(self.maze_size, self.maze_size)
        maze = render(noise)

        # Setting maze boundaries
        maze[0] = [99] * self.maze_size
        maze[-1] = [99] * self.maze_size
        for row in maze:
            row[0] = 99
            row[-1] = 99
        maze = np.array(maze, dtype=object)
        maze, start_door_grid = self.create_start_doors(maze, start_side)

        # Set the end points on the remaining three sides
        exit_side = ['top', 'bottom', 'left', 'right']
        exit_side.remove(start_side)
        for side in exit_side:
            if side == 'left':
                maze[self.maze_size // 2][0] = 94
                maze[(self.maze_size // 2) - 1][0] = 94

                maze[self.maze_size // 2][1] = 1
                maze[(self.maze_size // 2) - 1][1] = 1

            elif side == 'top':
                maze[0][self.maze_size // 2] = 95
                maze[0][(self.maze_size // 2) - 1] = 95

                maze[1][self.maze_size // 2] = 1
                maze[1][(self.maze_size // 2) - 1] = 1

            elif side == 'right':
                maze[self.maze_size // 2][self.maze_size - 1] = 96
                maze[(self.maze_size // 2) - 1][self.maze_size - 1] = 96

                maze[self.maze_size // 2][self.maze_size - 2] = 1
                maze[(self.maze_size // 2) - 1][self.maze_size - 2] = 1

            elif side == 'bottom':
                maze[self.maze_size - 1][self.maze_size // 2] = 97
                maze[self.maze_size - 1][(self.maze_size // 2) - 1] = 97

                maze[self.maze_size - 2][self.maze_size // 2] = 1
                maze[self.maze_size - 2][(self.maze_size // 2) - 1] = 1

        # Convert string to integers and lists
        self.converted_maze = []
        for row in maze:
            row_integers = [
                random.choice([1004, 1005, 1006, 1008, 1010, 1012]) if x == 1 and random.random() < 0.05 else int(x)
                for x in row
            ]
            self.converted_maze.append(row_integers)

        return self.converted_maze


    ### FIXME: labyrinth on vahel mingi topelt seinaga kui allapoole see avada
    def labyrinth_maze_generation(self, start_side):  # start_side - BOTTOM RIGHT LEFT TOP
        type_maze = 'labyrinth_maze'

        self.maze_size = self.maze_size
        maze = np.full((self.maze_size, self.maze_size), 99)  # numpy ver, [[99] * self.maze_size for _ in range(self.maze_size)]
        
        # func dfs teeb pathi, 98, mazei
        def dfs(row, col):
            if maze[row, col] not in GameConfig.CLOSED_DOOR_IDS.value and maze[row, col] not in GameConfig.OPEN_DOOR_IDS.value:
                maze[row, col] = 98

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
            random.shuffle(directions)

            for dr, dc in directions:
                new_row, new_col = row + 2 * dr, col + 2 * dc  # Move two steps in the chosen direction
                if 1 <= new_row < self.maze_size - 1 and 1 <= new_col < self.maze_size - 1 and maze[new_row, new_col] == 99:
                    
                    maze[row + dr, col + dc] = 98  # Mark the cell between current and next cell as a pathway
                    dfs(new_row, new_col)

        # Muudab vasakpoolse ja alumise eelviimase seina random 98/99'ks
        for i in range(1, self.maze_size - 1):
            choice = random.choices([98, 99])[0]
            maze[i, 1] = choice

        for i in range(1, self.maze_size - 1):
            choice = random.choices([98, 99])[0]
            maze[self.maze_size - 2, i] = choice

        maze, start_door_grid = self.create_start_doors(maze, start_side)

        # FIXME: fix this shit variable x dogass
        x = start_door_grid[0]
        dfs(x[0], x[1])

        # Enne ust teeb pathway et see blocked ei oleks. FIXME: see ei ole reliable solution
        maze[self.maze_size // 2, 1]            = 98
        maze[self.maze_size // 2 - 1, 1]        = 98
        maze[1, self.maze_size // 2]            = 98
        maze[1, self.maze_size // 2 - 1]        = 98
        maze[self.maze_size // 2, self.maze_size - 2]     = 98
        maze[self.maze_size // 2 - 1, self.maze_size - 2] = 98
        maze[self.maze_size - 2, self.maze_size // 2]     = 98
        maze[self.maze_size - 2, self.maze_size // 2 - 1] = 98

        exit_set = {'bottom', 'right', 'left', 'top'}
        exit_set.remove(start_side)

        for exit_side in exit_set:
            if exit_side == 'left':
                maze[self.maze_size // 2, 0] = 94
                maze[self.maze_size // 2 - 1, 0] = 94

            if exit_side == 'top':
                maze[0, self.maze_size // 2] = 95
                maze[0, self.maze_size // 2 - 1] = 95

            if exit_side == 'right':
                maze[self.maze_size // 2, self.maze_size - 1] = 96
                maze[self.maze_size // 2 - 1, self.maze_size - 1] = 96

            if exit_side == 'bottom':
                maze[self.maze_size - 1, self.maze_size // 2] = 97
                maze[self.maze_size - 1, self.maze_size // 2 - 1] = 97

        self.create_maze_items(maze)
        self.search_paths(maze, type_maze, start_side, start_door_grid)

        if self.create_save_puzzle == True:
            self.create_save_puzzle = False
            return maze

    def block_maze_generation(self, start_side):
        type_of_maze = 'block_maze'
        noise = self.block_maze_noise((self.maze_size, self.maze_size), self.resolution)
        noise_resized = resize(noise, (self.maze_size, self.maze_size), mode='reflect')
        maze = np.where(noise_resized > np.percentile(noise_resized, 75), 99, 98)

        maze[0, :] = maze[-1, :] = 99
        maze[:, 0] = maze[:, -1] = 99

        maze, start_door_grid = self.create_start_doors(maze, start_side)

        first_door, second_door = start_door_grid[0], start_door_grid[1]
        self.buffer_doors(maze, first_door, second_door, start_side)

        # Set the exit for random side
        sides = ['top', 'bottom', 'left', 'right']
        sides.remove(start_side)
        exit_side = random.choice(sides)
        random_position = random.randint(2, self.maze_size-3) # 0 kuni 39 on tegelikult, self.maze_size on 40 ehk 40-3 peaks olema solid failsafe

        # Set the exit point
        if exit_side == 'left':
            end_0 = (random_position    , 0)
            end_1 = (random_position + 1, 0)
            maze[end_0], maze[end_1] = 94, 94

        elif exit_side == 'top':
            end_0 = (0, random_position    )
            end_1 = (0, random_position + 1)
            maze[end_0], maze[end_1] = 95, 95

        elif exit_side == 'right':
            end_0 = (random_position    , self.maze_size - 1)
            end_1 = (random_position + 1, self.maze_size - 1)
            maze[end_0], maze[end_1] = 96, 96

        elif exit_side == 'bottom':
            end_0 = (self.maze_size - 1, random_position    )
            end_1 = (self.maze_size - 1, random_position + 1)
            maze[end_0], maze[end_1] = 97, 97
        
        exit_point = (end_0, end_1)
        print('Exit at', exit_point, exit_side)

        first_exit_door, second_exit_door = exit_point[0], exit_point[1]
        self.buffer_doors(maze, first_exit_door, second_exit_door, exit_side)
        
        # muudab maze datat, et string -> int -> list
        self.converted_maze = []
        for row in maze:
            row_integers = row.astype(int)  # muudab intis
            row_list = row_integers.tolist()  # muudab listiks
            self.converted_maze.append(row_list)

        maze = self.converted_maze

        self.create_maze_items(maze)
        self.search_paths(maze, type_of_maze, start_side, start_door_grid, exit_point)

        if self.create_save_puzzle:
            self.create_save_puzzle = False
            return maze


    def get_data(self, item, start_side):

        # 'labyrinth_maze', 'block_maze', 'blade_maze', 'final_maze', 'abandoned_glade'
        if item.endswith('maze'):
            if item == 'block_maze':
                return self.block_maze_generation(start_side)

            elif item == 'labyrinth_maze':
                return self.labyrinth_maze_generation(start_side)

            elif item == 'blade_maze':
                UniversalVariables.blades_spawned = True
                return self.file_to_maze(file_name=f'{item}.txt', side=start_side)

            elif item == 'final_maze':
                for row in UniversalVariables.map_list:
                    if 'final_maze' in row:
                        UniversalVariables.final_maze = True
                        return self.file_to_maze(file_name=f'{item}.txt', side=start_side)

        elif item == 'abandoned_glade':
            return self.abandoned_glade_generation(start_side)

        elif item == 'glade':
            # Glade'il pole start side
            return self.file_to_maze(file_name=f'{item}.txt')

        elif item == 'place':
            return self.placeholder

        else:
            # Handle other cases or raise an error
            raise ValueError(f"Unknown item type: {item}")


def glade_creation():
    glade_file_path = resource_path('glade.txt')
    with open(glade_file_path, 'r') as file:
        return [[int(x) for x in line.strip().replace('[', '').replace(']', '').split(',') if x.strip()]
                for line in file if line.strip()]

if __name__ == "__main__": ...
