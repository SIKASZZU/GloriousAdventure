import numpy as np

class MapData:
    width = 40
    height = 40
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

        # Initialize the wave function
        width = MapData.width
        height = MapData.height
        
        ### TODO: Kui tahta muuta maze kuju, siis muuta wave_function
            # Hetkel lihtsalt randomly genereerib ruute :D
        wave_function = np.random.choice([99, 1], size=(width, height), p=[0.3, 0.7])

        map_data = np.concatenate((wave_function, glade_data), axis=0)  # Säilitab teatud data kuju, kui concatenateida
        
        ### TODO: Teha eraldi function maze_creation ja siis veel map_creation
        
        map_data[0, :] = 99
        map_data[:, -1] = 99
        map_data[:, 0] = 99
        return map_data, glade_data
    
if __name__ == "__main__":
    MapData.glade_creation()