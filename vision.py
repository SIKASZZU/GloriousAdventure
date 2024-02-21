from variables import UniversalVariables
import math
from camera import Camera

class Vision:

    vision_blocking_boxes = []
    visible_boxes = []

    def testerino():

        ### ERALDI FUNC ### find_vision_blocking_boxes
        for vision_blocking_box in UniversalVariables.collision_boxes:
            if vision_blocking_box[2] != 0 or vision_blocking_box[3] != 0:
                if vision_blocking_box not in Vision.vision_blocking_boxes:
                    Vision.vision_blocking_boxes.append(vision_blocking_box)
            print(Vision.vision_blocking_boxes)
        
        ### ERALDI FUNC ### visible_boxes
        # Determine render range
        render_range = (UniversalVariables.screen_x + UniversalVariables.screen_y) // UniversalVariables.block_size // 5

        # Use the camera's position to determine the render range
        camera_grid_row = int((Camera.camera_rect.left + Camera.camera_rect.width / 2) // UniversalVariables.block_size)
        camera_grid_col = int((Camera.camera_rect.top + Camera.camera_rect.height / 2) // UniversalVariables.block_size)

        for visible_box in Vision.vision_blocking_boxes:
            box_x, box_y = visible_box[0], visible_box[1]
            # Check if box coordinates are within render range
            if (camera_grid_row - render_range <= box_x <= camera_grid_row + render_range and
                camera_grid_col - render_range <= box_y <= camera_grid_col + render_range):
                if visible_box[2] != 0 or visible_box[3] != 0:
                    if visible_box not in Vision.visible_boxes:
                        Vision.visible_boxes.append(visible_box)
            print(Vision.visible_boxes)

        ### TODO: Peab välja mõtlema, milline box on palyerile kõige lähedamal
    

    # Renderib boxid, mida player peaks n2gema
    def render_visible():
        visible_wall = []
        for angle in range(0, 360):
            # tähtsamad asjad, peab tegema ümber playeri 360 kiirt.
            radians = math.radians(angle)
            x_increment = math.cos(radians)
            y_increment = math.sin(radians)
            x = UniversalVariables.player_x
            y = UniversalVariables.player_y


            # for step in range(5):  # light radius peab olema render range 
            #     x += x_increment
            #     y += y_increment
            #     grid_x = int(x // UniversalVariables.block_size)
            #     grid_y = int(y // UniversalVariables.block_size)

    # renderib k6ik muu mustaks, mida player ei n2e
    def render_nothingness(): ...

if __name__ == '__main__':
    Vision.testerino()