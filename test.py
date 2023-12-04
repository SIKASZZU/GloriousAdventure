import numpy as np

class MapData:
    width = 40
    height = 40
    map_data = []

    # Create Glade
    @staticmethod
    def create_glade():
        glade_data = np.full((10, 10), 99)  # Example smaller glade (Modify as needed)
        return glade_data

    # Create Maze
    @staticmethod
    def create_maze():
        maze_data = np.full((20, 20), 98)  # Example larger maze (Modify as needed)
        return maze_data

    # Create Boss
    @staticmethod
    def create_boss():
        boss_data = np.full((8, 8), 97)  # Example smaller boss area (Modify as needed)
        return boss_data

    @staticmethod
    def map_creation():
        glade_data = MapData.create_glade()
        maze_data = MapData.create_maze()
        boss_data = MapData.create_boss()

        # Initialize map with default value 100 (empty space)
        MapData.map_data = np.full((MapData.width, MapData.height), 100)

        # Place Glade in the map (Modify as per your requirement)
        MapData.map_data[:glade_data.shape[0], :glade_data.shape[1]] = glade_data

        # Place Maze in the map (Modify as per your requirement)
        MapData.map_data[5:25, 5:25] = maze_data[:20, :20]

        # Place Boss in the map (Modify as per your requirement)
        MapData.map_data[10:18, 10:18] = boss_data

        return MapData.map_data


if __name__ == "__main__":
    map = MapData.map_creation()
    print(np.array(map))  # Print the generated map
