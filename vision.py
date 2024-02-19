from variables import UniversalVariables
import math

# Update walls list to contain corners of collision boxes
walls = []
for box in UniversalVariables.collision_boxes:
    x, y, width, height, _, offset_x, offset_y = box
    # Add corners of the collision box to walls list
    walls.extend([
        (x + offset_x, y + offset_y),
        (x + offset_x + width, y + offset_y),
        (x + offset_x, y + offset_y + height),
        (x + offset_x + width, y + offset_y + height)
    ])

def render_visible(surface, player_pos, walls):
    visible_walls = []
    for angle in range(0, 360):
        radians = math.radians(angle)
        x_increment = math.cos(radians)
        y_increment = math.sin(radians)
        x = player_pos[0]
        y = player_pos[1]
        for step in range(5):  # light radius peab olema render range 
            x += x_increment
            y += y_increment
            grid_x = int(x // UniversalVariables.block_size)
            grid_y = int(y // UniversalVariables.block_size)
            # Check if the current position is within a wall
            if (grid_x, grid_y) in walls:
                visible_walls.append((grid_x, grid_y))
                break

    # Draw only the walls that are visible
    for wall in walls:
        if wall in visible_walls:
            draw_wall(surface, wall)  # las teeb mingi listi, mille render func impordib ning ss renderib tolle listi lihtsalt