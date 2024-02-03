from map import MapData

class NewMaze:
    def spawn_maze_at_location(self, location):
        placements = {4: 'left', 3: 'right', 1: 'bottom', 2: 'top'}
        if location in placements:  #  location on key ; placements[location] annab value
            start_side = placements[location]
        else: print('mapupdate.py error, location not in placements')

        self.terrain_data = MapData.map_creation(location, start_side)

