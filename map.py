import os
import sys
import numpy as np
from skimage.transform import resize
from collections import deque
import random
import copy
from variables import UniversalVariables


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MapData:
    ### FIXME: See peab olema [[None] * 39 for _ in range(40)]
    placeholder = [[None] * 39 for _ in range(40)]

    maze_size = 40
    resolution = (maze_size, maze_size)  # Adjusted resolution of Perlin noise for more distributed walls

    old = copy.deepcopy(UniversalVariables.map_list)  # Use deepcopy to avoid reference issues

    create_save_puzzle = None
    converted_maze = []

    if UniversalVariables.debug_mode:
        _puzzle_pieces = 20
        _keyholders = 20
        _loot = 20
    else:
        _puzzle_pieces = 6  # on vaja kindlasti rohkem, kui kaheksa
        _keyholders = 4     # on vaja kaheksa
        _loot = random.randint(3, 5)  # _loot = random.randint(3, 5)

    def glade_creation():
        glade_file_path = resource_path('glade.txt')
        with open(glade_file_path, 'r') as file:
            return [[int(x) for x in line.strip().replace('[', '').replace(']', '').split(',') if x.strip()]
                    for line in file if line.strip()]


    @staticmethod
    def file_to_maze(file_name: str, side: str = None):
        if side is None:
            maze_file_path = resource_path('glade.txt')
        else:
            maze_file_path = resource_path(file_name)

        maze = []
        with open(maze_file_path, 'r') as file:
            maze = [[int(x) if x.strip().lower() != 'none' else None
                     for x in line.strip().replace('[', '').replace(']', '').split(',') if x.strip()]
                    for line in file if line.strip()]
        size = len(maze)

        # Set the start point
        if side == 'left':
            start_0 = (size // 2, 0)
            start_1 = (size // 2 - 1, 0)
            maze[start_0[0]][start_0[1]], maze[start_1[0]][start_1[1]] = 90, 90
        elif side == 'top':
            start_0 = (0, size // 2)
            start_1 = (0, size // 2 - 1)
            maze[start_0[0]][start_0[1]], maze[start_1[0]][start_1[1]] = 91, 91
        elif side == 'right':
            start_0 = (size // 2, size - 1)
            start_1 = (size // 2 - 1, size - 1)
            maze[start_0[0]][start_0[1]], maze[start_1[0]][start_1[1]] = 92, 92
        elif side == 'bottom':
            start_0 = (size - 1, size // 2)
            start_1 = (size - 1, size // 2 - 1)
            maze[start_0[0]][start_0[1]], maze[start_1[0]][start_1[1]] = 93, 93

        # compiler
        if side == None:
            pass
        else:
            sides = ['top', 'bottom', 'left', 'right']
            sides.remove(side)
            for side in sides:

                if side == 'left':
                    end_0 = ((size // 2), 0)
                    end_1 = ((size // 2) - 1, 0)
                    maze[end_0[0]][end_0[1]], maze[end_1[0]][end_1[1]] = 94, 94

                elif side == 'top':
                    end_0 = (0, (size // 2))
                    end_1 = (0, (size // 2) - 1)
                    maze[end_0[0]][end_0[1]], maze[end_1[0]][end_1[1]] = 95, 95

                elif side == 'right':
                    end_0 = ((size // 2), size - 1)
                    end_1 = ((size // 2) - 1, size - 1)
                    maze[end_0[0]][end_0[1]], maze[end_1[0]][end_1[1]] = 96, 96

                elif side == 'bottom':
                    end_0 = (size - 1, (size // 2))
                    end_1 = (size - 1, (size // 2) - 1)
                    maze[end_0[0]][end_0[1]], maze[end_1[0]][end_1[1]] = 97, 97

            return maze


    def final_maze_generation(start_side):
        UniversalVariables.final_maze = True
        return MapData.file_to_maze(file_name='final_maze.txt', side=start_side)


    def blade_maze_generation(start_side):
        UniversalVariables.blades_spawned = True
        return MapData.file_to_maze(file_name='blade_maze.txt', side=start_side)

    def abandoned_glade_generation(start_side):
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

        size = MapData.maze_size
        noise = generate_glade_terrain(size, size)
        maze = render(noise)

        # Setting maze boundaries
        maze[0] = ['99'] * size
        maze[-1] = ['99'] * size
        for row in maze:
            row[0] = '99'
            row[-1] = '99'

        # Set the start point
        if start_side == 'left':
            maze[size // 2][0] = "90"
            maze[(size // 2) - 1][0] = "90"

            maze[size // 2][1] = "1"
            maze[(size // 2) - 1][1] = "1"

        elif start_side == 'top':
            maze[0][size // 2] = "91"
            maze[0][(size // 2) - 1] = "91"

            maze[1][size // 2] = "1"
            maze[1][(size // 2) - 1] = "1"

        elif start_side == 'right':
            maze[size // 2][size - 1] = "92"
            maze[(size // 2) - 1][size - 1] = "92"

            maze[size // 2][size - 2] = "1"
            maze[(size // 2) - 1][size - 2] = "1"

        elif start_side == 'bottom':
            maze[size - 1][size // 2] = "93"
            maze[size - 1][(size // 2) - 1] = "93"

            maze[size - 2][size // 2] = "1"
            maze[size - 2][(size // 2) - 1] = "1"

        # Set the end points on the remaining three sides
        sides = ['top', 'bottom', 'left', 'right']
        sides.remove(start_side)
        for side in sides:
            if side == 'left':
                maze[size // 2][0] = "94"
                maze[(size // 2) - 1][0] = "94"

                maze[size // 2][1] = "1"
                maze[(size // 2) - 1][1] = "1"

            elif side == 'top':
                maze[0][size // 2] = "95"
                maze[0][(size // 2) - 1] = "95"

                maze[1][size // 2] = "1"
                maze[1][(size // 2) - 1] = "1"

            elif side == 'right':
                maze[size // 2][size - 1] = "96"
                maze[(size // 2) - 1][size - 1] = "96"

                maze[size // 2][size - 2] = "1"
                maze[(size // 2) - 1][size - 2] = "1"

            elif side == 'bottom':
                maze[size - 1][size // 2] = "97"
                maze[size - 1][(size // 2) - 1] = "97"

                maze[size - 2][size // 2] = "1"
                maze[size - 2][(size // 2) - 1] = "1"

        # Convert string to integers and lists
        MapData.converted_maze = []
        for row in maze:
            row_integers = [
                random.choice([1004, 1005, 1006, 1008, 1010, 1012]) if x == 1 and random.random() < 0.05 else int(x)
                for x in row
            ]
            MapData.converted_maze.append(row_integers)

        return MapData.converted_maze


    ### FIXME: labyrinth on vahel mingi topelt seinaga kui allapoole see avada
    def labyrinth_maze_generation(start_side):  # start_side - BOTTOM RIGHT LEFT TOP
        type_maze = 'labyrinth_maze'

        size = MapData.maze_size
        maze = [[99] * size for _ in range(size)]

        def dfs(row, col):
            maze[row][col] = 98

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
            random.shuffle(directions)

            for dr, dc in directions:
                new_row, new_col = row + 2 * dr, col + 2 * dc  # Move two steps in the chosen direction
                if 1 <= new_row < size - 1 and 1 <= new_col < size - 1 and maze[new_row][new_col] == 99:
                    maze[row + dr][col + dc] = 98  # Mark the cell between current and next cell as a pathway
                    dfs(new_row, new_col)

        # Muudab vasakpoolse ja alumise eelviimase seina random 98/99'ks
        for i in range(1, size - 1):
            choice = random.choices([98, 99])[0]
            maze[i][1] = choice

        for i in range(1, size - 1):
            choice = random.choices([98, 99])[0]
            maze[size - 2][i] = choice

        # Set the start point
        if start_side == 'left':
            start_0 = (size // 2, 0)
            start_1 = (size // 2 - 1, 0)
            dfs(start_0[0], start_0[1])
            maze[start_0[0]][start_0[1]], maze[start_1[0]][start_1[1]] = 90, 90
        
        elif start_side == 'top':
            start_0 = (0, size // 2)
            start_1 = (0, size // 2 - 1)
            dfs(start_0[0], start_0[1])
            maze[start_0[0]][start_0[1]], maze[start_1[0]][start_1[1]] = 91, 91
        
        elif start_side == 'right':
            start_0 = (size // 2, size - 1)
            start_1 = (size // 2 - 1, size - 1)
            dfs(start_0[0], start_0[1])
            maze[start_0[0]][start_0[1]], maze[start_1[0]][start_1[1]] = 92, 92
        
        elif start_side == 'bottom':
            start_0 = (size - 1, size // 2)
            start_1 = (size - 1, size // 2 - 1)
            dfs(start_0[0], start_0[1])
            maze[start_0[0]][start_0[1]], maze[start_1[0]][start_1[1]] = 93, 93

        # Enne ust teeb pathway et see blocked ei oleks. FIXME: see ei ole reliable solution
        maze[size // 2][1]            = 98
        maze[size // 2 - 1][1]        = 98
        maze[1][size // 2]            = 98
        maze[1][size // 2 - 1]        = 98
        maze[size // 2][size - 2]     = 98
        maze[size // 2 - 1][size - 2] = 98
        maze[size - 2][size // 2]     = 98
        maze[size - 2][size // 2 - 1] = 98

        exit_set = {'bottom', 'right', 'left', 'top'}
        exit_set.remove(start_side)

        for exit_side in exit_set:

            if exit_side == 'left':
                maze[size // 2][0] = 94
                maze[size // 2 - 1][0] = 94

            if exit_side == 'top':
                maze[0][size // 2] = 95
                maze[0][size // 2 - 1] = 95

            if exit_side == 'right':
                maze[size // 2][size - 1] = 96
                maze[size // 2 - 1][size - 1] = 96

            if exit_side == 'bottom':
                maze[size - 1][size // 2] = 97
                maze[size - 1][size // 2 - 1] = 97

        MapData.create_maze_items(maze, size)
        MapData.search_paths(maze, type_maze, start_side)

        if MapData.create_save_puzzle:
            MapData.create_save_puzzle = False
            return maze


    @staticmethod
    def block_maze_generation(start_side):
        type_of_maze = 'block_maze'
        size = MapData.maze_size
        resolution = MapData.resolution
        noise = MapData.block_maze_noise((size, size), resolution)
        noise = MapData.block_maze_noise((size, size), resolution)
        noise_resized = resize(noise, (size, size), mode='reflect')
        maze = np.where(noise_resized > np.percentile(noise_resized, 75), '99',
                        '98')  # threshold adjusted to create more walls

        # outer walls one block in must be pathway, value 98.
        for row in range(size):
            maze[row][1] = 98
            maze[row][size - 2] = 98

        for col in range(size):
            maze[1][col] = 98
            maze[size - 2][col] = 98

        ### TODO: siin on mingi string numbrid, neid pole vaja ning siis pole vaja ka "row_integers = row.astype(int)"
        maze[0, :] = maze[-1, :] = '99'
        maze[:, 0] = maze[:, -1] = '99'

        # Set the start point
        if start_side == 'left':
            start_0 = ((size // 2), 0)
            start_1 = ((size // 2) - 1, 0)
            maze[start_0], maze[start_1] = "90", "90"
        elif start_side == 'top':
            start_0 = (0, (size // 2))
            start_1 = (0, (size // 2) - 1)
            maze[start_0], maze[start_1] = "91", "91"

        elif start_side == 'right':
            start_0 = ((size // 2), size - 1)
            start_1 = ((size // 2) - 1, size - 1)
            maze[start_0], maze[start_1] = "92", "92"

        elif start_side == 'bottom':
            start_0 = (size - 1, (size // 2))
            start_1 = (size - 1, (size // 2) - 1)
            maze[start_0], maze[start_1] = "93", "93"

        # Set the end points on the remaining three sides
        sides = ['top', 'bottom', 'left', 'right']
        sides.remove(start_side)
        for side in sides:

            if side == 'left':
                end_0 = ((size // 2), 0)
                end_1 = ((size // 2) - 1, 0)
                maze[end_0], maze[end_1] = "94", "94"

            elif side == 'top':
                end_0 = (0, (size // 2))
                end_1 = (0, (size // 2) - 1)
                maze[end_0], maze[end_1] = "95", "95"

            elif side == 'right':
                end_0 = ((size // 2), size - 1)
                end_1 = ((size // 2) - 1, size - 1)
                maze[end_0], maze[end_1] = "96", "96"

            elif side == 'bottom':
                end_0 = (size - 1, (size // 2))
                end_1 = (size - 1, (size // 2) - 1)
                maze[end_0], maze[end_1] = "97", "97"

        # muudab maze datat, et string -> int -> list
        MapData.converted_maze = []
        for row in maze:
            row_integers = row.astype(int)
            row_list = row_integers.tolist()
            MapData.converted_maze.append(row_list)

        MapData.create_maze_items(MapData.converted_maze, size)
        MapData.search_paths(MapData.converted_maze, type_of_maze, start_side)

        if MapData.create_save_puzzle:
            MapData.create_save_puzzle = False
            return MapData.converted_maze


    def create_maze_items(maze, size):

        def spawn_key(maze, puzzle_x, puzzle_y):
            if random.random() < 0.1: maze[puzzle_x][puzzle_y] = 10   # 10% full key
            elif random.random() < 0.5: maze[puzzle_x][puzzle_y] = 12 # 50% key top half
            else: maze[puzzle_x][puzzle_y] = 13                       # else, 50%, key bottom half

        # Maze puzzle pieces
        for i in range(MapData._puzzle_pieces):
            while True:
                puzzle_x = random.randint(3, (size - 3))
                puzzle_y = random.randint(3, (size - 3))
                if maze[puzzle_x][puzzle_y] == 99:
                    if not MapData.is_dead_end(maze, puzzle_x, puzzle_y):
                        spawn_key(maze, puzzle_x, puzzle_y)
                        break

        # Maze keyholders
        for i in range(MapData._keyholders):
            while True:
                keyholder_x = random.randint(3, (size - 3))
                keyholder_y = random.randint(3, (size - 3))
                if maze[keyholder_x][keyholder_y] == 99:
                    if not MapData.is_dead_end(maze, keyholder_x, keyholder_y):
                        maze[keyholder_x][keyholder_y] = 981
                        break

        # Maze loot barrels
        if random.choice([True]):
            for i in range(MapData._loot):
                while True:
                    loot_x = random.randint(3, (size - 3))
                    loot_y = random.randint(3, (size - 3))
                    if maze[loot_x][loot_y] == 99:
                        if not MapData.is_dead_end(maze, loot_x, loot_y):
                            maze[loot_x][loot_y] = 1001
                            break

        return maze      


    def is_dead_end(maze, x, y):
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

    def is_valid(x, y, maze):
        return 0 <= x < len(maze) and 0 <= y < len(maze[x]) and maze[x][y] != 99

    def find_path_bfs(maze, start, end):
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
                    if MapData.is_valid(new_x, new_y, maze):
                        new_path = path + [(new_x, new_y)]
                        queue.append(((new_x, new_y), new_path))

        return None


    def search_paths(maze, type_of_maze, start_side):
        """ maze is list. type_of_maze is block_maze, labyrinth_maze, final_maze, blade_maze etc. """

        special_positions = []
        start_positions = [(38, 19), (38, 20)]  # y, x
        end_positions = [(19, 38), (20, 38),
                         (1, 19), (1, 20),
                         (19, 1), (20, 1),
                         (38, 19), (38, 20)]

        # Check paths from each start to each end and special positions
        for start in start_positions:
            for end in end_positions + special_positions:
                path = MapData.find_path_bfs(maze, start, end)
                if path is None:
                    print(f"No path found from {start} to {end}")
                    MapData.create_save_puzzle = False

                else:
                    print(f"Path found from {start} to {end}")
                    MapData.create_save_puzzle = True
                    
                    # check visually, kas path on valid v6i mitte.
                    #  for tuple in path:
                    #      maze[tuple[0]][tuple[1]] = 2

        if MapData.create_save_puzzle == False:
            if type_of_maze == 'block_maze':
                maze = MapData.block_maze_generation(start_side)
                
            elif type_of_maze == 'labyrinth_maze':
                maze = MapData.labyrinth_maze_generation(start_side)
            MapData.search_paths(maze)


    @staticmethod
    def get_data(item, start_side):

        # 'labyrinth_maze', 'block_maze', 'blade_maze', 'final_maze', 'abandoned_glade'


        if item.endswith('maze'):
            if item == 'block_maze':
                return MapData.block_maze_generation(start_side)

            elif item == 'labyrinth_maze':
                return MapData.labyrinth_maze_generation(start_side)

            elif item == 'blade_maze':
                UniversalVariables.blades_spawned = True
                return MapData.file_to_maze(file_name=f'{item}.txt', side=start_side)

            elif item == 'final_maze':
                for row in UniversalVariables.map_list:
                    if 'final_maze' in row:
                        UniversalVariables.final_maze = True
                        return MapData.file_to_maze(file_name=f'{item}.txt', side=start_side)


        elif item == 'abandoned_glade':
            return MapData.abandoned_glade_generation(start_side)

        elif item == 'glade':
            # Glade'il pole start side
            return MapData.file_to_maze(file_name=f'{item}.txt')

        elif item == 'place':
            return MapData.placeholder

        else:
            # Handle other cases or raise an error
            raise ValueError(f"Unknown item type: {item}")


    def map_list_to_map(self, start_side='bottom'):
        difference = []
        new = UniversalVariables.map_list

        if MapData.old != []:
            max_length = max(len(new), len(MapData.old))

            for row_index in range(max_length):
                if row_index >= len(MapData.old):
                    for col_index, item in enumerate(new[row_index]):
                        difference.append(item)
                else:
                    new_row = new[row_index]
                    old_row = MapData.old[row_index] if row_index < len(MapData.old) else []

                    for col_index, item in enumerate(new_row):
                        if col_index >= len(old_row) or item not in old_row:
                            difference.append(item)

        if self.terrain_data is None:
            # If there's no existing terrain_data, generate new map data from scratch
            new_map_data = []
            for sublist in UniversalVariables.map_list:
                combined_rows = None
                for item in sublist:
                    if item == 'glade':
                        current_data = MapData.glade_creation()
                    else:
                        current_data = MapData.get_data(item, start_side)

                    if combined_rows is None:
                        combined_rows = current_data
                    else:
                        combined_rows = [row1 + row2 for row1, row2 in zip(combined_rows, current_data)]
                new_map_data.extend(combined_rows)
            self.terrain_data = new_map_data
            MapData.old = copy.deepcopy(UniversalVariables.map_list)  # Update MapData.old here if needed

        return self.terrain_data


if __name__ == "__main__": ...
