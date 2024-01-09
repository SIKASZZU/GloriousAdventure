import numpy as np
import random
import functools

class MapData:
    width = 40
    height = 40
    maze_location = 0  # 0 default map, 1 ylesse, 2 alla, 3 vasakule, 4 paremale

    map_data = []
    maze_data = []
    glade_data = []
    new_map_data = []
    new_row = []
    maze_fill = np.full((width, height), 98)  # filler maze, et zipping ilusti tootaks.

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

    ### TODO: mazei uks või algus oleks alati ühes teatud kohas. Gladei ava juures!
    # Generate maze using recursive backtracking algorithm
    @staticmethod
    @functools.lru_cache(maxsize=None)  # None - unlimited cache
    def maze_generation():
        size = 40
        maze = [[99] * size for _ in range(size)]

        def dfs(row, col):
            maze[row][col] = 98  # Mark the current cell as a pathway

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
            random.shuffle(directions)

            for dr, dc in directions:
                new_row, new_col = row + 2 * dr, col + 2 * dc  # Move two steps in the chosen direction
                if 0 <= new_row < size and 0 <= new_col < size and maze[new_row][new_col] == 99:
                    maze[row + dr][col + dc] = 98  # Mark the cell between current and next cell as a pathway
                    dfs(new_row, new_col)

        # Set player starting position at the bottom middle
        player_position = (size - 1, size // 2)

        # Generate pathways from player position
        dfs(player_position[0], player_position[1])

        # Create openings in the outer walls at exit positions
        exits = [
            (0, size // 2),          # Top side, middle of the wall
            (size // 2, 0),          # Left side, middle of the wall
            (size // 2, size - 1),   # Right side, middle of the wall
            (size - 1, size // 2)    # Bottom side, middle of the wall (entrance)
        ]
        for row, col in exits:
            maze[row][col] = 0

        # Create fewer walls within the maze to make it more navigable
        for _ in range(size * size // 100):  # Adjust the density of walls based on preference
            row, col = random.randint(1, size - 2), random.randint(1, size - 2)
            maze[row][col] = 99

        return maze

    # print("\nPlayer starting position:", player_position)
    # print("Exit positions:", exits)


    def spawn_puzzle():
        ... ### TODO: Pst lambine ruut, nr 98, on puzzle. ss ei pea mingi pathfinderi tegema.

    def map_creation():
        map_data = MapData.map_data
        maze_location = MapData.maze_location

        # support mazeid
        maze_fill = MapData.maze_fill
        maze_data = maze_fill.tolist()

        maze_start = MapData.maze_generation()
        glade_data = MapData.glade_creation()
        maze_data = MapData.maze_generation()

        new_map_data = MapData.new_map_data
        new_row = MapData.new_row

        if not map_data:  # list is empty
            map_data = maze_start + glade_data
        else: pass

        # Lisab glade_data ja maze_data kokku ning paneb selle teatud kohta
        print(f'maze_location: {maze_location},\n {map_data} \n\n {maze_data}')
        
        if maze_location == 1:  # add new maze to: top
            new_map_data = maze_data + map_data

        elif maze_location == 2:  # add new maze to: bottom
            new_map_data = map_data + maze_data

        elif maze_location == 3:  # add new maze to: left
            new_map_data = []
            for maze_row, map_row in zip(maze_data, map_data):
                new_row = maze_row + map_row
                new_map_data.append(new_row)
    
        elif maze_location == 4:  # add new maze to: right
            new_map_data = []
            for maze_row, map_row in zip(maze_data, map_data):
                new_row = map_row + maze_row
                new_map_data.append(new_row)

        else: print(f'maze_location: {maze_location}; no new maze appended')

        # If there are extra rows in map_data that are not covered by maze_data
        remaining_rows_count = len(map_data) - len(maze_data)
        maze_fill = MapData.maze_fill
        maze_fill = maze_fill.tolist()
    
        ### TODO: Kui remaining_rows on negatiivne, siis tuleb lisada filler_maze yles poole
            # kui midagi on seal olemas juba, ss fillerit ei saa lisada.

        if remaining_rows_count != 0:
            remaining_rows = map_data[len(maze_data):]
            for maze_fill_row, remaining_row in zip(maze_fill, remaining_rows):
                if maze_location == 3: new_row = maze_fill_row + remaining_row
                if maze_location == 4: new_row = remaining_row + maze_fill_row
                new_map_data.append(new_row)

        if maze_location != 0:
            map_data = new_map_data  # Et ei writiks koguaeg map_datat üle. Muidu maze_location = 0 on valge map

        print(f'\nmaze_location: {maze_location}')

        ### TODO: Listid pole sama dimensioonidega. Yks on suurem kui teine.

        ### TODO: K6igile mazecountidel on erinev, kuhu sein peaks tekkima.

        MapData.map_data = map_data
        return MapData.map_data

if __name__ == "__main__":
    MapData.map_creation()
    MapData.maze_generation()
