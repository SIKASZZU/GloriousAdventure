from map import MapData


class UpdateMapData:

    def spawn_maze_at_location(location):
        # if playerx < 1800, left
        if location == 4:
            start_side = 'left'
        else:
            print('bug')
        MapData.map_creation(location, start_side)
