# https://github.com/XT60/Dynamic-lights-2D
# https://www.youtube.com/watch?v=fc3nnG2CG8U

# ^ temalt saab 6ppust v6tta


import pygame
from variables import UniversalVariables

class Vision:
    walls_list = []
    block_size = UniversalVariables.block_size
    def find_walls():
        glade = UniversalVariables.glade_data
        # find wall's grid
        for i, row in enumerate(glade):
            for j, value in enumerate(row):
                if value == 99:
                    Vision.walls_list.append((i, j))
        print('walls', Vision.walls_list, '\n')
        
        # find wall's coordinates
        ### TODO: see sama pask uuesti, hakkab arvutama seinade asukohta. aga see peaks kuskil tehtud olema
        Vision.wall_points(Vision.walls_list)

    

    def wall_points(walls_list):
        # "Collision_box": [0, 0, 1, 1]
        wall_points_list = []
        for i, item in enumerate(walls_list):
            wall_NE_point = Vision.block_size * 1
            wall_SE_point = Vision.block_size * 1
            wall_NW_point = Vision.block_size * 0
            wall_SW_point = Vision.block_size * 0
            wall_points = (wall_NW_point, wall_SW_point, wall_NE_point, wall_SE_point)
            wall_points_list.append(wall_points)
        print(wall_points_list)


if __name__ == "__main__":
    Vision.find_walls()