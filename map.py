import numpy as np

class MapData:
    width = 40
    height = 40
    def glade_creation():

        map_data = []

        with open('glade.txt', 'r') as file:
            for line in file:
                cleaned_line = line.strip()
                if cleaned_line:
                    cleaned_line = cleaned_line.replace('[', '').replace(']', '')
                    row = [int(x) for x in cleaned_line.split(',') if x.strip()]
                    map_data.append(row)

        # Initialize the wave function
        width = MapData.width
        height = MapData.height
        wave_function = np.random.choice([99, 1], size=(width, height), p=[0.3, 0.7])
        #print(wave_function)

        ### Kuidas teada, kuhu maze tekib olenevalt kuidas appendida

        #if position == "above":
        #    return maze_list + map_data
        #elif position == "below":
        #    return map_data + maze_list
        #elif position == "left":
        #    return [new_row + original_row for new_row, original_row in zip(maze_list, map_data)]
        #elif position == "right":
        #    return [original_row + new_row for original_row, new_row in zip(map_data, maze_list)]

        ###
        map_data = np.concatenate((wave_function, map_data), axis=0)  # Concatenate above
        #map_data = wave_function + map_data
        print(map_data)
        
        map_data[0, :] = 99
        map_data[-1, :] = 99
        map_data[:, -1] = 99
        map_data[:, 0] = 99
        return map_data
MapData.glade_creation()