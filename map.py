import numpy as np

class MapData:
    width = 40
    height = 40
    maze_count = 4

    map_data = []
    maze_data = []
    glade_data = []

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
        ### TODO: Mazei põrand oleks stone, mitte terrain.
        maze_data_np_array = np.random.choice([99, 98], size=(width, height), p=[0.3, 0.7])
        maze_data = maze_data_np_array.tolist()
        return maze_data
    
    def map_creation():
        map_data = MapData.map_data
        maze_count = MapData.maze_count
        maze_data = MapData.maze_creation()
        glade_data = MapData.glade_creation()

        # Lisab glade_data ja maze_data kokku ning paneb selle teatud kohta
        
        if MapData.maze_count == 0:  # add new maze to: top
            map_data = maze_data + glade_data
            print(f'process:\n {maze_count},\n {map_data} \n=\n {maze_data} \n+\n {glade_data}')

        if MapData.maze_count == 1:  # add new maze to: bottom
            map_data = glade_data + maze_data
            print(f'process:\n {maze_count},\n {map_data} \n=\n {maze_data} \n+\n {glade_data}')

        if MapData.maze_count == 3:  # add new maze to: left
            map_data = [new_row + original_row for new_row, original_row in zip(maze_data, glade_data)]
            print(f'process:\n {maze_count},\n {map_data} \n=\n {maze_data} \n+\n {glade_data}')

        if MapData.maze_count == 4:  # add new maze to: right
            map_data = [original_row + new_row for original_row, new_row in zip(glade_data, maze_data)]
            print(f'process:\n {maze_count},\n {map_data} \n=\n {maze_data} \n+\n {glade_data}')

        ### TODO: Error props, kui map_data list on juba maze_data + glade_data. 
            # Error tuleneb sellest, et need listid pole sama dimensioonidega. Yks on suurem kui teine.

        # Muudab maze 22red seinteks.
        #map_data[0, :] = 99  # top
        #map_data[:, -1] = 99  # parem kylg
        #map_data[:, 0] = 99  # vasak kylg
        #map_data[-1, :] = 99  # alumine kylg  # vist ei t66ta

        MapData.map_data = map_data
        return MapData.map_data

if __name__ == "__main__":
    print('lol')