import numpy as np
from skimage.transform import resize

class MapData:
    width = 40
    height = 40
    maze_location = 0  # 0 default map, 1 ylesse, 2 alla, 3 vasakule, 4 paremale

    map_data = []
    maze_data = []
    glade_data = []
    new_map_data = []
    new_row = []
    maze_fill = np.full((width, height), 98)  # filler maze, et zipping ilusti tootaks.

    start_side = 'bottom'
    maze_size = 40
    resolution = (40, 40)  # Adjusted resolution of Perlin noise for more distributed walls

    # Create glade
    def glade_creation():
        glade_data = []

        with open('glade.txt', 'r') as file:
            for line in file:
                cleaned_line = line.strip()
                if cleaned_line:
                    cleaned_line = cleaned_line.replace('[', '').replace(']', '')
                    row = [int(x) for x in cleaned_line.split(',') if x.strip()]
                    glade_data.append(row)
        
        return glade_data

    def maze_generation(shape, res):
        def f(t):
            return 1*t**7 - 5*t**0 + 1*t**1

        grid = np.mgrid[0:res[0],0:res[1]].transpose(1, 2, 0)
        grid = grid / res

        gradients = np.random.rand(res[0] + 1, res[1] + 1, 2)
        gradients /= np.linalg.norm(gradients, axis=2, keepdims=True)

        g00 = gradients[:-1,:-1]
        g10 = gradients[1:,:-1]
        g01 = gradients[:-1,1:]
        g11 = gradients[1:,1:]

        t = grid - grid.astype(int)
        fade_t = f(t)

        n00 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1])) * g00, axis=2)
        n10 = np.sum(np.dstack((grid[:,:,0] - 1, grid[:,:,1])) * g10, axis=2)
        n01 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1] - 1)) * g01, axis=2)
        n11 = np.sum(np.dstack((grid[:,:,0] - 1, grid[:,:,1] - 1)) * g11, axis=2)

        n0 = n00 * (1 - fade_t[:,:,0]) + n10 * fade_t[:,:,0]
        n1 = n01 * (1 - fade_t[:,:,0]) + n11 * fade_t[:,:,0]

        noise = np.sqrt(2) * (n0 * (1 - fade_t[:,:,1]) + n1 * fade_t[:,:,1])
        return noise

    def create_maze_with_perlin_noise(start_side):
        size = MapData.maze_size 
        resolution = MapData.resolution 
        noise = MapData.maze_generation((size, size), resolution)
        noise_resized = resize(noise, (size, size), mode='reflect')
        maze = np.where(noise_resized > np.percentile(noise_resized, 75), '99', '98')  # threshold adjusted to create more walls

        # Ensure outer walls
        maze[0, :] = maze[-1, :] = '99'
        maze[:, 0] = maze[:, -1] = '99'

        # Set the start point
        if start_side == 'top':
            start = (0, (size // 2))
        elif start_side == 'bottom':
            start = (size-1, (size // 2))
        elif start_side == 'left':
            start = ((size // 2), 0)
        elif start_side == 'right':
            start = ((size // 2), size-1)
        maze[start] = '7'

        # Set the end points on the remaining three sides
        sides = ['top', 'bottom', 'left', 'right']
        sides.remove(start_side)
        for side in sides:
            if side == 'top':
                end = (0, (size // 2))
            elif side == 'bottom':
                end = (size-1, (size // 2))
            elif side == 'left':
                end = ((size // 2), 0)
            elif side == 'right':
                end = ((size // 2), size-1)
            maze[end] = '7'

        # convert <class 'numpy.ndarray'> to list
        converted_maze = []
        for row in maze:
            row_integers = row.astype(int)
            row_list = row_integers.tolist()
            converted_maze.append(row_list)

        print('mazetype', type(converted_maze))
        return converted_maze

    def spawn_puzzle():
        ... ### TODO: Pst lambine ruut, nr 98, on puzzle.

    def map_creation():
        map_data = MapData.map_data
        maze_location = MapData.maze_location

        # support mazeid
        maze_fill = MapData.maze_fill
        maze_data = maze_fill.tolist()

        start_side = MapData.start_side
        maze_start = MapData.create_maze_with_perlin_noise(start_side)
        glade_data = MapData.glade_creation()
        maze_data = MapData.create_maze_with_perlin_noise(start_side)

        new_map_data = MapData.new_map_data
        new_row = MapData.new_row

        if not map_data:  # list is empty
            map_data = maze_start + glade_data
        else: pass

        # Lisab glade_data ja maze_data kokku ning paneb selle teatud kohta
        print(f'maze_location: {maze_location},\n {map_data} \n\n {maze_data}')
        
        if maze_location == 1:  # add new maze to: top
            new_map_data = maze_data + map_data

        elif maze_location == 2:  # add new maze to: bottom
            new_map_data = map_data + maze_data

        elif maze_location == 3:  # add new maze to: left
            new_map_data = []
            for maze_row, map_row in zip(maze_data, map_data):
                new_row = maze_row + map_row
                new_map_data.append(new_row)
    
        elif maze_location == 4:  # add new maze to: right
            new_map_data = []
            for maze_row, map_row in zip(maze_data, map_data):
                new_row = map_row + maze_row
                new_map_data.append(new_row)

        else: print(f'maze_location: {maze_location}; no new maze appended')

        # If there are extra rows in map_data that are not covered by maze_data
        remaining_rows_count = len(map_data) - len(maze_data)
        maze_fill = MapData.maze_fill
        maze_fill = maze_fill.tolist()
    
        ### TODO: Kui remaining_rows on negatiivne, siis tuleb lisada filler_maze yles poole
            # kui midagi on seal olemas juba, ss fillerit ei saa lisada.

        if remaining_rows_count != 0:
            remaining_rows = map_data[len(maze_data):]
            for maze_fill_row, remaining_row in zip(maze_fill, remaining_rows):
                if maze_location == 3: new_row = maze_fill_row + remaining_row
                if maze_location == 4: new_row = remaining_row + maze_fill_row
                new_map_data.append(new_row)

        if maze_location != 0:
            map_data = new_map_data  # Et ei writiks koguaeg map_datat üle. Muidu maze_location = 0 on valge map

        print(f'\nmaze_location: {maze_location}')

        MapData.map_data = map_data
        return MapData.map_data

if __name__ == "__main__":
    # MapData.map_creation()
    MapData.create_maze_with_perlin_noise(MapData.start_side)
