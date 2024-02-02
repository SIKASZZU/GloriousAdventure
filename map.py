import numpy as np
from skimage.transform import resize
from collections import deque
import random
from printingdata import print_data_by_lines

class MapData:
    width = 40
    height = 40
    maze_location = 0  # 0 default map, 1 ylesse, 2 alla, 3 vasakule, 4 paremale
    start_side = 'bottom'

    map_data = []
    maze_data = []
    glade_data = []  # map creationi juures vaja
    new_map_data = []  # map creationi juures vaja
    new_row = []

    maze_fill = np.full((width, height), None)  # filler maze, et zipping ilusti tootaks.
    new_maze_data = []  # Loob uue mazei selle lisamiseks
    maze_size = 40
    resolution = (40, 40)  # Adjusted resolution of Perlin noise for more distributed walls

    puzzle_pieces: list[tuple, tuple, tuple] = []
    create_save_puzzle = None
    converted_maze = []
    
    repetition_lock = 0

    # Create glade
    def glade_creation():
        glade_data = []

        with open('glade.txt', 'r') as file:
            for line in file:
                cleaned_line = line.strip()
                if cleaned_line:
                    cleaned_line = cleaned_line.replace('[', '').replace(']', '')
                    row = [int(x) for x in cleaned_line.split(',') if x.strip()]
                    glade_data.append(row)
        
        return glade_data

    def maze_generation(shape, res):
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

    def create_maze_with_perlin_noise(start_side):
        size = MapData.maze_size 
        resolution = MapData.resolution 
        noise = MapData.maze_generation((size, size), resolution)
        noise_resized = resize(noise, (size, size), mode='reflect')
        maze = np.where(noise_resized > np.percentile(noise_resized, 75), '99', '98')  # threshold adjusted to create more walls

        # outer walls one block in must be pathway, value 98.
        # BEFORE ensuring outer walls
        for row in range(size):
            maze[row][1] = 98
            maze[row][size - 2] = 98

        for col in range(size):
            maze[1][col] = 98
            maze[size - 2][col] = 98

        # Ensure outer walls
        # AFTER outer wall one block must be pathway
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
            maze[start_0], maze[start_1]= "91", "91"

        elif start_side == 'right':
            start_0 = ((size // 2), size-1)
            start_1 = ((size // 2) - 1, size-1)
            maze[start_0], maze[start_1]= "92", "92"

        elif start_side == 'bottom':
            start_0 = (size-1, (size // 2))
            start_1 = (size-1, (size // 2) - 1)
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
                end_0 = ((size // 2), size-1)
                end_1 = ((size // 2) - 1, size-1)
                maze[end_0], maze[end_1] = "96", "96"

            elif side == 'bottom':
                end_0 = (size-1, (size // 2))
                end_1 = (size-1, (size // 2) - 1)
                maze[end_0], maze[end_1] = "97", "97"

        # muudab maze datat, et string -> int -> list
        MapData.converted_maze = []
        for row in maze:
            row_integers = row.astype(int)
            row_list = row_integers.tolist()
            MapData.converted_maze.append(row_list)

        # Maze's puzzle pieces
        MapData.puzzle_pieces = []
        for i in range(3):
            xxxx = random.randint(3, (size - 3))
            yyyy = random.randint(3, (size - 3))
            MapData.converted_maze[xxxx][yyyy] = 7
            if not (xxxx, yyyy) in MapData.puzzle_pieces:
                MapData.puzzle_pieces.append((xxxx, yyyy))

        MapData.search_paths(MapData.converted_maze)
        if MapData.create_save_puzzle:
            return MapData.converted_maze


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


    def search_paths(maze):
        special_positions = []

        # y, x
        start_positions = [(38, 19), (38, 20)]

        end_positions = [(19, 38), (20, 38),
                        (1, 19), (1, 20),
                        (19, 1), (20, 1),
                        (38, 19), (38, 20)]

        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == 9:
                    special_positions.append((i, j))

        # Check paths from each start to each end and special positions
        for start in start_positions:
            for end in end_positions + special_positions:
                path = MapData.find_path_bfs(maze, start, end)
                if path is None:
                    print(f"No path found from {start} to {end}")
                    MapData.create_save_puzzle = False

                else:
                    # for i in range(len(maze)):
                    #     for j in range(len(maze[i])):
                    #         if maze[i][j] == 7:
                    #             for (x, y) in path:
                    #                 MapData.converted_maze[x][y] = 1
                    for (x, y) in start_positions + end_positions:
                        MapData.converted_maze[x][y] = 2
                    MapData.create_save_puzzle = True


        if MapData.create_save_puzzle == False:
            maze = MapData.create_maze_with_perlin_noise(MapData.start_side)
            MapData.search_paths(maze)


    def spawn_puzzle():
        ... ### TODO: Pst lambine ruut, nr 98, on puzzle.


    def map_creation(location = 0, start_side_new = 'bottom'):
        MapData.repetition_lock += 1
        # lisada +1 mingi sitt systeem, et kui terrain_data hakatakse variables kutsuma, siis siin m6tleb valja kas see on esimen ekord v6i teine.
        
        if MapData.repetition_lock == 1:
            maze_location = 0
            start_side = 'bottom'
        elif MapData.repetition_lock >= 2:
            maze_location = location
            start_side = start_side_new

        print('repetitionlock count:', MapData.repetition_lock)
        print('func map_creation maze_location', maze_location, 'start_side', start_side, 'start_side_new', start_side_new,'\n')

        map_data = MapData.map_data  # current map data

        # support mazes
        maze_fill = MapData.maze_fill
        new_maze_data = MapData.create_maze_with_perlin_noise(start_side)

        # starting mazes
        maze_start = MapData.create_maze_with_perlin_noise(start_side)
        glade_data = MapData.glade_creation()

        # new map craetion
        new_map_data = MapData.new_map_data
        new_row = MapData.new_row

        # alguses, kui map datat pole veel olemas
        if not map_data:  # list is empty   ### TODO: saab ymber kirjutada repitition lockiga
            map_data = maze_start + glade_data
        else: pass

        # Lisab glade_data ja maze_data kokku ning paneb selle teatud kohta
        #print(f'maze_location: {maze_location},\n {map_data} \n\n {new_maze_data}')
        
        if maze_location == 1:  # add new maze to: top
            new_map_data = new_maze_data + map_data

        elif maze_location == 2:  # add new maze to: bottom
            new_map_data = map_data + new_maze_data

        elif maze_location == 3:  # add new maze to: left
            new_map_data = []
            for maze_row, map_row in zip(new_maze_data, map_data):
                new_row = maze_row + map_row
                new_map_data.append(new_row)
    
        elif maze_location == 4:  # add new maze to: right
            new_map_data = []
            for maze_row, map_row in zip(new_maze_data, map_data):
                new_row = map_row + maze_row
                new_map_data.append(new_row)

        else: print(f'maze_location: {maze_location}; no new maze appended')

        # If there are extra rows in map_data that are not covered by new_maze_data
        remaining_rows_count = len(map_data) - len(new_maze_data)
        maze_fill = MapData.maze_fill
        maze_fill = maze_fill.tolist()
        print(maze_fill)

        ### TODO: Kui remaining_rows on negatiivne, siis tuleb lisada filler_maze yles poole
            # kui midagi on seal olemas juba, ss fillerit ei saa lisada.

        if remaining_rows_count != 0:
            remaining_rows = map_data[len(new_maze_data):]
            for maze_fill_row, remaining_row in zip(maze_fill, remaining_rows):
                if maze_location == 3: new_row = maze_fill_row + remaining_row
                if maze_location == 4: new_row = remaining_row + maze_fill_row
                new_map_data.append(new_row)

        if maze_location != 0:
            map_data = new_map_data  # Et ei writiks koguaeg map_datat üle. Muidu maze_location = 0 on valge map

        #print(f'\nmaze_location: {maze_location}')

        MapData.map_data = map_data
        return MapData.map_data

if __name__ == "__main__":
    # maze = MapData.create_maze_with_perlin_noise(MapData.start_side)
    maze_location = 1

    terrain_data = MapData.map_creation()  # map data
    glade_data = MapData.glade_creation()  # glade data
    print('terraindata\n', terrain_data, '\n')
