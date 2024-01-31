from map import MapData

class NewMaze:
    def spawn_maze_at_location(self, location):
        if location == 4:
            start_side = 'left'
        else:
            print('bug')


        ### l2him door


        # arvutab locationi j2rgi 2ra, kus asub start position
        # if playerx < 1800, left
            # location = UniversalVariables.location
        # start_side = UniversalVariables.start_side




        self.terrain_data = MapData.map_creation(location, start_side)
