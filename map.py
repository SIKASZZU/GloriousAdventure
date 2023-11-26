import numpy as np

class MapData:
    width = 40
    height = 40
    
    # Create glade
    def glade_creation():

        glade_data = []
        map_data = []

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
        
        ### TODO: Kui tahta muuta maze kuju, siis muuta maze_data. Hetkel genereerib lihtsalt random ruute
        ### TODO: Mazei põrand oleks stone, mitte terrain.
        maze_data = np.random.choice([99, 98], size=(width, height), p=[0.3, 0.7])
        
        return maze_data
    
    def map_creation():
        maze_data = MapData.maze_creation()
        glade_data = MapData.glade_creation()

        # Lisab glade_data ja maze_data kokku. Hetkel paneb selle mazei peale.
        map_data = np.concatenate((maze_data, glade_data), axis=0)  # Säilitab teatud data kuju, kui concatenateida

        # Muudab maze 22red seinteks.
        map_data[0, :] = 99
        map_data[:, -1] = 99
        map_data[:, 0] = 99

        return map_data

if __name__ == "__main__":
    MapData.glade_creation()