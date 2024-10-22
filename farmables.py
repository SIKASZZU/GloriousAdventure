from variables import UniversalVariables, GameConfig
import random

class Farmable:
    def __init__(self, object_id, random_range, growth_time):
        self.object_id = object_id
        self.random_range = random_range
        self.growth_time = growth_time

    def get_growth_time(self):
        random_a, random_b = self.random_range
        return self.growth_time - random.randint(random_a, random_b)

    def advance_stage(self, current_object_id):
        stage_transitions = {
            69: 70, 72: 73, 75: 76, 78: 79,
            70: 7, 73: 71, 76: 74, 79: 77
        }
        return stage_transitions.get(current_object_id, current_object_id)


class Wheat(Farmable):
    def __init__(self):
        super().__init__(GameConfig.WHEAT_STAGES.value, UniversalVariables.wheat_minus_random_range, UniversalVariables.wheat_stage_growth_time)


class Carrot(Farmable):
    def __init__(self):
        super().__init__(GameConfig.CARROT_STAGES.value, UniversalVariables.carrot_minus_random_range, UniversalVariables.carrot_stage_growth_time)


class Corn(Farmable):
    def __init__(self):
        super().__init__(GameConfig.CORN_STAGES.value, UniversalVariables.corn_minus_random_range, UniversalVariables.corn_stage_growth_time)


class Potato(Farmable):
    def __init__(self):
        super().__init__(GameConfig.POTATO_STAGES.value, UniversalVariables.potato_minus_random_range, UniversalVariables.potato_stage_growth_time)


class Farm:
    def __init__(self):
        self.farmables = {
            GameConfig.WHEAT_STAGES.value: Wheat(),
            GameConfig.CARROT_STAGES.value: Carrot(),
            GameConfig.CORN_STAGES.value: Corn(),
            GameConfig.POTATO_STAGES.value: Potato(),
        }

    def process_stage(self, object_id, grid, x, y):
        if object_id in GameConfig.FARMABLE_STAGES.value:
            farmable = self.farmables.get(object_id)
            if not farmable:
                return

            found = False

            for index, (pos, current_object_id, timer) in enumerate(UniversalVariables.farmable_stage_list):
                if pos == grid:
                    found = True

                    if timer > 0:
                        timer -= 1

                    if timer == 0:
                        current_object_id = farmable.advance_stage(current_object_id)
                        timer = farmable.get_growth_time()
                        self.terrain_data[y][x] = current_object_id

                    UniversalVariables.farmable_stage_list[index] = (pos, current_object_id, timer)
                    if current_object_id in GameConfig.FARMABLES.value:
                        self.remove_items_by_pos(pos)
                    break

            if not found:
                growth_time = farmable.get_growth_time()
                UniversalVariables.farmable_stage_list.append((grid, object_id, growth_time))
                print(growth_time)

    def remove_items_by_pos(self, pos):
        if current_object_id in GameConfig.FARMABLES.value:
            remove_items_by_pos(pos)
        pass
