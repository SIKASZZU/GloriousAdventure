from map import MapData

class test:
    def spawn_maze_at_location(self, location):
        # arvutab locationi j2rgi 2ra, kus asub start position
        # if playerx < 1800, left
        if location == 4:
            start_side = 'left'
        else:
            print('bug')
            # location = UniversalVariables.location
        # start_side = UniversalVariables.start_side

        terrain_data_new = MapData.map_creation(location, start_side)
        self.terrain_data = terrain_data_new
