import numpy as np

class MapData:
    width = 40
    height = 40
    maze_count = 0  # 0 default map, 1 ylesse, 2 alla, 3 vasakule, 4 paremale

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

    # Creating maze
    def maze_creation():
        width = MapData.width
        height = MapData.height
        maze_data = MapData.maze_data

        ### TODO: Kui tahta muuta maze kuju, siis muuta maze_data. Hetkel genereerib lihtsalt random ruute
        maze_data_np_array = np.random.choice([99, 98], size=(width, height), p=[0.35, 0.65])

        maze_data_np_array[0, :] = 99  # Top wall
        maze_data_np_array[-1, :] = 99  # Bottom wall
        maze_data_np_array[:, 0] = 99  # Left wall
        maze_data_np_array[:, -1] = 99  # Right wall

        return maze_data_np_array.tolist()
    
    def map_creation():
        map_data = MapData.map_data
        maze_count = MapData.maze_count

        maze_fill = MapData.maze_fill
        maze_data = maze_fill.tolist()

        maze_data = MapData.maze_creation()
        glade_data = MapData.glade_creation()
        maze_start = MapData.maze_creation()

        new_map_data = MapData.new_map_data
        new_row = MapData.new_row

        map_data = maze_start + glade_data

        if not map_data:  # list is empty
            map_data = glade_data
        else: pass

        # Lisab glade_data ja maze_data kokku ning paneb selle teatud kohta
        print(f'maze_count: {maze_count},\n {map_data} \n\n {maze_data}')
        
        if maze_count == 1:  # add new maze to: top
            new_map_data = maze_data + map_data

        elif maze_count == 2:  # add new maze to: bottom
            new_map_data = map_data + maze_data

        elif maze_count == 3:  # add new maze to: left
            new_map_data = []
            for maze_row, map_row in zip(maze_data, map_data):
                new_row = maze_row + map_row
                new_map_data.append(new_row)
    
        elif maze_count == 4:  # add new maze to: right
            new_map_data = []
            for maze_row, map_row in zip(maze_data, map_data):
                new_row = map_row + maze_row
                new_map_data.append(new_row)

        else: print(f'maze_count: {maze_count}; no new maze appended')

        # If there are extra rows in map_data that are not covered by maze_data
        remaining_rows_count = len(map_data) - len(maze_data)
        maze_fill = MapData.maze_fill
        maze_fill = maze_fill.tolist()
    
        ### TODO: Kui remaining_rows on negatiivne, siis tuleb lisada filler_maze yles poole
            # kui midagi on seal olemas juba, ss fillerit ei saa lisada.
        if remaining_rows_count != 0:
            remaining_rows = map_data[len(maze_data):]
            for maze_fill_row, remaining_row in zip(maze_fill, remaining_rows):
                if maze_count == 3: new_row = maze_fill_row + remaining_row
                if maze_count == 4: new_row = remaining_row + maze_fill_row
                new_map_data.append(new_row)

        if maze_count != 0:
            map_data = new_map_data  # Et ei writiks koguaeg map_datat üle. Muidu maze_count = 0 on valge map

        print(f'\nmaze_count: {maze_count}')

        ### TODO: Listid pole sama dimensioonidega. Yks on suurem kui teine.

        ### TODO: K6igile mazecountidel on erinev, kuhu sein peaks tekkima.

        ### TODO: Generate a maze until a valid path is found.
        ### TODO: Use the pathfinding algorithm to ensure there's a valid path through the maze.
        ### TODO: Return the maze data with a valid path.


        #https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96


        # PATH FINDER
        # from collections import deque
        #
        # def is_valid_move(maze, row, col):
        #     rows = len(maze)
        #     cols = len(maze[0])
        #     return 0 <= row < rows and 0 <= col < cols and maze[row][col] != 99  # Check boundaries and walls
        #
        # def bfs(maze, start_row, start_col):
        #     rows = len(maze)
        #     cols = len(maze[0])
        #     visited = set()
        #     queue = deque([(start_row, start_col)])
        #
        #     while queue:
        #         current_row, current_col = queue.popleft()
        #         visited.add((current_row, current_col))
        #
        #         # Check if current position is an end point
        #         if maze[current_row][current_col] == 100:
        #             maze[current_row][current_col] = 0  # Mark it as visited
        #
        #         # Define possible movements (up, down, left, right)
        #         moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        #
        #         for move in moves:
        #             new_row = current_row + move[0]
        #             new_col = current_col + move[1]
        #
        #             if is_valid_move(maze, new_row, new_col) and (new_row, new_col) not in visited:
        #                 queue.append((new_row, new_col))
        #
        # def solve_maze(maze):
        #     start_row, start_col = None, None
        #
        #     # Finding the starting point
        #     for i in range(len(maze)):
        #         for j in range(len(maze[0])):
        #             if maze[i][j] == 101:
        #                 start_row, start_col = i, j
        #                 break
        #
        #     if start_row is None or start_col is None:
        #         print("Start point not found!")
        #         return
        #
        #     bfs(maze, start_row, start_col)
        #
        #     # Check if all end points are visited
        #     for i in range(len(maze)):
        #         for j in range(len(maze[0])):
        #             if maze[i][j] == 100:
        #                 print("Not all end points are reachable.")
        #                 return
        #
        #     print("All end points are reachable!")
        #
        # # Your maze data
        # maze = [
        #     # Your maze data here
        #     # Add other rows as needed
        # ]
        #
        # solve_maze(maze)

        MapData.map_data = map_data
        return MapData.map_data

if __name__ == "__main__":
    MapData.map_creation()
    print(MapData.map_data)
    print(MapData.map_data)
    print(MapData.map_data)
