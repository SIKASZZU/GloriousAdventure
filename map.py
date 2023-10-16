import numpy as np
from perlin_noise import PerlinNoise

class MapData:

    def glade_creation():

        map_data = []

        with open('glade.txt', 'r') as file:
            for line in file:
                cleaned_line = line.strip()
                if cleaned_line:
                    cleaned_line = cleaned_line.replace('[', '').replace(']', '')
                    row = [int(x) for x in cleaned_line.split(',') if x.strip()]
                    map_data.append(row)

        return map_data