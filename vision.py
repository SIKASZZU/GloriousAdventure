# https://github.com/XT60/Dynamic-lights-2D
# https://www.youtube.com/watch?v=fc3nnG2CG8U

# ^ temalt saab 6ppust v6tta

from variables import UniversalVariables

class Vision:

    walls_list = []
    block_size = UniversalVariables.block_size

    def find_walls():
        for collision_box_x, collision_box_y, collision_box_width, collision_box_height, object_id, collision_box_offset_x, collision_box_offset_y in UniversalVariables.collision_boxes:
            obj_collision_box = (collision_box_x, collision_box_y, collision_box_width, collision_box_height, object_id, collision_box_offset_x, collision_box_offset_y)
            if object_id == 99:
                x = obj_collision_box[0]
                y = obj_collision_box[1]
                wall_location = (x, y)
                Vision.walls_list.append(wall_location)

            Vision.wall_points(Vision.walls_list)


    def wall_points(walls_list):
        wall_points_list = []
        for index, item in enumerate(walls_list):
            
            wall_NE_point = item[0] + Vision.block_size
            wall_SE_point = item[1] + Vision.block_size
            wall_NW_point = item[0]
            wall_SW_point = item[1]

            wall_points = (wall_NW_point, wall_SW_point, wall_NE_point, wall_SE_point)
            wall_points_list.append(wall_points)
        #return wall_points_list


if __name__ == "__main__":
    Vision.find_walls()