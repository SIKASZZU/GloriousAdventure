import numpy as np

class MapData:
    width = 40
    height = 40
    maze_count = 3  # 0 ylesse, 1 alla, 2 vasakule, 3 paremale

    map_data = []
    maze_data = []
    glade_data = []
    maze_fill = np.full((width, height), 98)  # test

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
        maze_data = maze_data_np_array.tolist()
        return maze_data  # type = list
    
    def map_creation():
        map_data = MapData.map_data
        maze_count = MapData.maze_count

        maze_fill = MapData.maze_fill
        maze_data = maze_fill.tolist()

        maze_data = MapData.maze_creation()
        glade_data = MapData.glade_creation()
        maze_start = MapData.maze_creation()

        map_data = maze_start + glade_data

        if not map_data:  # list is empty
            map_data = glade_data
        else: pass

        # Lisab glade_data ja maze_data kokku ning paneb selle teatud kohta
        print(f'process: {maze_count},\n {map_data} \n\n {maze_data}')
        
        if maze_count == 0:  # add new maze to: top
            new_map_data = maze_data + map_data

        elif maze_count == 1:  # add new maze to: bottom
            new_map_data = map_data + maze_data

        elif maze_count == 2:  # add new maze to: left
            new_map_data = []
            for maze_row, map_row in zip(maze_data, map_data):
                new_row = maze_row + map_row
                new_map_data.append(new_row)
    
        elif maze_count == 3:  # add new maze to: right
            new_map_data = []
            for maze_row, map_row in zip(maze_data, map_data):
                new_row = map_row + maze_row
                new_map_data.append(new_row)

        # If there are extra rows in map_data that are not covered by maze_data
        remaining_rows_count = len(map_data) - len(maze_data)
        maze_fill = MapData.maze_fill
        maze_fill = maze_fill.tolist()
    
        ### TODO: Kui remaining_rows on negatiivne, siis tuleb lisada filler_maze yles poole
            # kui midagi on seal olemas juba, ss fillerit ei saa lisada.
        if remaining_rows_count != 0:
            remaining_rows = map_data[len(maze_data):]
            for maze_fill_row, remaining_row in zip(maze_fill, remaining_rows):
                if maze_count == 2: new_row = maze_fill_row + remaining_row
                if maze_count == 3: new_row = remaining_row + maze_fill_row
                new_map_data.append(new_row)

        map_data = new_map_data
        print(f'\nprocess: {maze_count}, mapdata RESULT: {map_data}')

        ### TODO: Error props, kui map_data list on juba maze_data + glade_data. 
        ### TODO: Listid pole sama dimensioonidega. Yks on suurem kui teine.

        ### TODO: K6igile mazecountidel on erinev, kuhu sein peaks tekkima.
        # Muudab maze 22red seinteks.
        #map_data[0, :] = 99  # top
        #map_data[:, -1] = 99  # parem kylg
        #map_data[:, 0] = 99  # vasak kylg
        #map_data[-1, :] = 99  # alumine kylg  # vist ei t66ta


        ### TODO: Generate a maze until a valid path is found.
        ### TODO: Use the pathfinding algorithm to ensure there's a valid path through the maze.
        ### TODO: Return the maze data with a valid path.


        # PATH FINDER
        # from collections import deque

        # directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # def is_valid(x, y, maze):
        #     return 0 <= x < len(map_data) and 0 <= y < len(map_data[x]) and maze[x][y] != '*'

        # def find_path_bfs(maze, start, end):
        #     queue = deque([(start, [])])
        #     visited = set()

        #     while queue:
        #         (x, y), path = queue.popleft()

        #         if (x, y) == end:
        #             return path

        #         if (x, y) not in visited:
        #             visited.add((x, y))

        #             for dx, dy in directions:
        #                 new_x, new_y = x + dx, y + dy
        #                 if (new_x, new_y) not in visited:
        #                     if is_valid(new_x, new_y, maze):
        #                         new_path = path + [(new_x, new_y)]
        #                         queue.append(((new_x, new_y), new_path))

        #     return None

        # start_pos = None
        # end_pos = None

        # with open("cave_maps/cave300x300.txt") as f:
        #     map_data = [l.strip() for l in f.readlines() if len(l) > 1]

        # def search_bfs(map):
        #     for i in range(len(map)):
        #         for j in range(len(map[i])):
        #             if map[i][j] == 's':   ## start on block 100
        #                 start_pos = (i, j)
        #             elif map[i][j] == 'D':
        #                 end_pos = (i, j)
        #     path = find_path_bfs(map, start_pos, end_pos)

        #     if path is not None:
        #         for i in range(len(map)):
        #             row = ""
        #             for j in range(len(map[i])):
        #                 if map[i][j] == "D":
        #                     row += "D"
        #                 elif (i, j) in path:
        #                     row += "."
        #                 else:
        #                     row += map[i][j]
        #             print(row)
        #     else:
        #         print("No path found")

        # # search_bfs(map_data)
        # search_bfs(map_data)





        MapData.map_data = map_data
        return MapData.map_data

if __name__ == "__main__":
    MapData.map_creation()