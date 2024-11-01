from variables import UniversalVariables, GameConfig
import random
from typing import Tuple

def remove_items_by_pos(pos_to_remove: Tuple[int, int]) -> None:
    UniversalVariables.farmable_stage_list[:] = [item for item in UniversalVariables.farmable_stage_list if item[0] != pos_to_remove]

def farming(self, x: int, y: int, grid: Tuple[int, int]) -> Tuple[str, int, str]:
    object_id = self.terrain_data[y][x]
    stage_growth_time, random_range = None, None

    if object_id in GameConfig.WHEAT_STAGES.value:
        stage_growth_time = UniversalVariables.wheat_stage_growth_time
        random_range = UniversalVariables.wheat_minus_random_range
    elif object_id in GameConfig.CARROT_STAGES.value:
        stage_growth_time = UniversalVariables.carrot_stage_growth_time
        random_range = UniversalVariables.carrot_minus_random_range
    elif object_id in GameConfig.CORN_STAGES.value:
        stage_growth_time = UniversalVariables.corn_stage_growth_time
        random_range = UniversalVariables.corn_minus_random_range
    elif object_id in GameConfig.POTATO_STAGES.value:
        stage_growth_time = UniversalVariables.potato_stage_growth_time
        random_range = UniversalVariables.potato_minus_random_range

    found = False

    for index, (pos, current_object_id, timer) in enumerate(UniversalVariables.farmable_stage_list):
        if pos == grid:
            found = True
            if timer > 0:
                timer -= 1

            if timer == 0:
                next_stage = {
                    69: 70, 72: 73, 75: 76, 78: 79,
                    70: 7, 73: 71, 76: 74, 79: 77
                }
                current_object_id = next_stage.get(current_object_id, current_object_id)
                timer = stage_growth_time - random.randint(*map(int, random_range))
                self.terrain_data[y][x] = current_object_id

            UniversalVariables.farmable_stage_list[index] = (pos, current_object_id, timer)
            if current_object_id in GameConfig.FARMABLES.value:
                remove_items_by_pos(pos)
            break

    if object_id in GameConfig.FARMABLES.value:
        return 'Farmland', 107, GameConfig.GROUND_IMAGE.value

    if not found and stage_growth_time and random_range:
        growth_time = stage_growth_time - random.randint(*map(int, random_range))
        UniversalVariables.farmable_stage_list.append((grid, object_id, growth_time))

    return 'Farmland', 107, GameConfig.GROUND_IMAGE.value
