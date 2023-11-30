import numpy as np

class MapData:
    width = 40
    height = 40
    maze_count = 3

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
            # Error tuleneb sellest, et need listid pole sama dimensioonidega. Yks on suurem kui teine.

        ### TODO: K6igile mazecountidel on erinev, kuhu sein peaks tekkima.
        # Muudab maze 22red seinteks.
        #map_data[0, :] = 99  # top
        #map_data[:, -1] = 99  # parem kylg
        #map_data[:, 0] = 99  # vasak kylg
        #map_data[-1, :] = 99  # alumine kylg  # vist ei t66ta

        MapData.map_data = map_data
        return MapData.map_data

if __name__ == "__main__":
    MapData.map_creation()