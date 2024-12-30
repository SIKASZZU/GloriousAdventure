import random

from variables import UniversalVariables, GameConfig
from objects import ObjectManagement
from items import search_item_from_items, ConsumableItem
from text import Fading_text


def is_click_inside_player_rect(self):

    if not self.camera.click_position:  # Return'ib kui click_position on tühi
        return False

    if None in self.camera.click_position:  # Return'ib kui click_position'is on None
        return False

    player_x = self.player_update.player_rect[0] + UniversalVariables.offset_x
    player_y = self.player_update.player_rect[1] + UniversalVariables.offset_y

    # Vaatab, kas click on player rect'i sees
    click_within_x = player_x < self.camera.click_position[0] < player_x + self.player_update.player_rect[2]
    click_within_y = player_y < self.camera.click_position[1] < player_y + self.player_update.player_rect[3]

    return click_within_x and click_within_y  # Return'ib tulemuse


def probably(chance):
    return random.random() < chance


def find_number_in_list_of_lists(list_of_lists):

    choices = []
    # FIXME: 96,7 on broken millegi pärast.

    # FIXME: Otsib doore, mida pole olemas veel

    chosen_id = random.choice([door_id for door_id in GameConfig.CLOSED_DOOR_IDS.value if door_id != 977])
    print('chosen id', chosen_id)
    for row_index, sublist in enumerate(list_of_lists):
        for col_index, element in enumerate(sublist):
            if element == chosen_id:
                grid = row_index, col_index
                if grid not in choices:
                    choices.append(grid)  # Number found, add to all possible choices
            
    if choices:
        UniversalVariables.geiger_chosen_grid = random.choice(choices)
        print('choices', choices, 'chose, ', UniversalVariables.geiger_chosen_grid)
        return UniversalVariables.geiger_chosen_grid  # Return grid
    
    return None  # Number not found, return None


class ItemFunctionality:
    def __init__(self, td, entity, player, paudio, pupdate, cam, inv):
        self.terrain_data = td
        self.entity = entity
        self.player = player
        self.player_audio = paudio
        self.player_update = pupdate
        self.camera = cam
        self.inv = inv

        self.last_strength_read = str
        self.maze_counter       = 0
        self.strength_counter   = 0

    def update(self):
        if self.strength_counter > 0:
            self.strength_counter -= 1
            return

        self.current_equipped()
        return


    def find_signal_strength(self):
        """ Vaatab pathi yhe random ukseni ning selle jargi returnib. """

        # FIND GRID
        if UniversalVariables.geiger_chosen_grid == None:
            find_number_in_list_of_lists(self.terrain_data)

        if UniversalVariables.geiger_chosen_grid == None:
            return
                    
        # FIND PATH TO GRID
        grid_x = int(UniversalVariables.player_x // UniversalVariables.block_size)
        grid_y = int(UniversalVariables.player_y // UniversalVariables.block_size)
        
        # pathfind player -> random chosen door
        player_grid = (grid_y, grid_x)
        path = self.entity.find_path_bfs(UniversalVariables.geiger_chosen_grid, player_grid)

        # RETURN SIGNAL STRENGTH
        if not path:
            return None    # Path doesn't exist

        if len(path) >= 50:        return 'low'     # long path
        elif 50 > len(path) >= 10: return 'medium'  
        elif 10 > len(path) >= 1:  return 'high'    # short path

    def current_equipped(self):
        """ Argument on item, mille funktsiooni kutsutakse. """

        equipped_item = UniversalVariables.current_equipped_item
        if equipped_item == 'Geiger':

            if UniversalVariables.maze_counter != self.maze_counter:
                UniversalVariables.geiger_chosen_grid = None
                self.maze_counter = UniversalVariables.maze_counter

            strength = self.find_signal_strength()

            # heli, kui strength tase muutub
            if strength != self.last_strength_read:
                self.last_strength_read = strength
                ... # audio

            # peamine heli pathi pikkuse tottu
            if not strength:
                UniversalVariables.print_debug_text('None')
                self.strength_counter = 500
                ... # Ootab 5 sekki - teeb resa vms

            if strength == 'low':
                UniversalVariables.print_debug_text('low')
                ... # audio
                
            elif strength == 'medium':
                UniversalVariables.print_debug_text('low')
                ... # audio

            elif strength == 'high':
                UniversalVariables.print_debug_text('low')
                ... # audio

            # heli, mis on alati
                ... # audio

            # lambine heli (segaja), random funci jargi aktiveerub yheks loopiks
            if random.random() > 0.1:
                ... # audio

        #********* ITEMS < CLICK PLAYER TO USE *********#
        if not is_click_inside_player_rect(self):
            return

        if UniversalVariables.interaction_delay < UniversalVariables.interaction_delay_max:
            if UniversalVariables.debug_mode:
                print(f'Item delay: {UniversalVariables.interaction_delay} < {UniversalVariables.interaction_delay_max} ')
            return

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

        cure = search_item_from_items(type=ConsumableItem, item_name_or_id=equipped_item, target_attribute="cure")
        poisonous = search_item_from_items(type=ConsumableItem, item_name_or_id=equipped_item, target_attribute="poisonous")
        healing_amount = search_item_from_items(type=ConsumableItem, item_name_or_id=equipped_item, target_attribute="healing_amount")
        satisfaction_gain = search_item_from_items(type=ConsumableItem, item_name_or_id=equipped_item, target_attribute="satisfaction_gain")
        thirst_resistance = search_item_from_items(type=ConsumableItem, item_name_or_id=equipped_item, target_attribute="thirst_resistance")
        hunger_resistance = search_item_from_items(type=ConsumableItem, item_name_or_id=equipped_item, target_attribute="hunger_resistance")

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

        if cure:
            UniversalVariables.interaction_delay = 0
            UniversalVariables.serum_active = True  # see funktsionaalsus j2tkub status.py-is
            ObjectManagement.remove_object_from_inv(self, equipped_item)

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

        if poisonous:
            UniversalVariables.interaction_delay = 0

            if probably(35 / 100):
                UniversalVariables.player_poisoned = True

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

        if healing_amount:
            UniversalVariables.interaction_delay = 0

            player_healed = self.player.health.heal(healing_amount)
            if player_healed:  ObjectManagement.remove_object_from_inv(self, equipped_item)
            if UniversalVariables.player_bleeding == True:
                if probably(35 / 100):
                    UniversalVariables.player_bleeding = False

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

        if thirst_resistance and satisfaction_gain:
            UniversalVariables.interaction_delay = 0
            ObjectManagement.remove_object_from_inv(self, equipped_item)  # v6tab joodud itemi 2ra

            if self.player.thirst.current_thirst >= self.player.thirst.max_thirst and UniversalVariables.thirst_resistance > 0:
                Fading_text.re_display_fading_text("If you drink too much you might get sick!")
                if probably(15 / 100):
                    UniversalVariables.player_poisoned = True

            # Arvutab uue thirsti 'current + söödud itemi Gain'
            new_thirst = self.player.thirst.current_thirst + satisfaction_gain

            # Et playeri thirst ei läheks üle maxi ega alla min
            if new_thirst >= self.player.thirst.max_thirst:
                self.player.thirst.current_thirst = self.player.thirst.max_thirst

            elif new_thirst <= self.player.thirst.min_thirst:
                self.player.thirst.current_thirst = self.player.thirst.min_thirst

            else:
                self.player.thirst.current_thirst = new_thirst

            self.player_audio.drinking_audio(self)
            self.camera.click_position = ()

            # Kui thirst_resistance on alla 0 või alla eelneva thirst_resistance siis resetib thirst_resistance
            if UniversalVariables.thirst_resistance > thirst_resistance or 0 > UniversalVariables.thirst_resistance:
                return

            UniversalVariables.thirst_resistance = thirst_resistance

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

        elif hunger_resistance and satisfaction_gain:
            UniversalVariables.interaction_delay = 0
            ObjectManagement.remove_object_from_inv(self, equipped_item)  # v6tab s66dud itemi 2ra

            if self.player.hunger.current_hunger >= self.player.hunger.max_hunger and UniversalVariables.hunger_resistance > 0:
                Fading_text.re_display_fading_text("If you eat too much you might get sick!")
                if probably(15 / 100):
                    UniversalVariables.player_poisoned = True

            # Arvutab uue hungeri 'current + söödud itemi Gain'
            new_hunger = self.player.hunger.current_hunger + satisfaction_gain

            # Et playeri hunger ei läheks üle maxi ega alla min
            if new_hunger >= self.player.hunger.max_hunger:
                self.player.hunger.current_hunger = self.player.hunger.max_hunger

            elif new_hunger <= self.player.hunger.min_hunger:
                self.player.hunger.current_hunger = self.player.hunger.min_hunger

            else:
                self.player.hunger.current_hunger = new_hunger

            self.player_audio.eating_audio(self)
            self.camera.click_position = ()

            # Kui hunger_resistance on alla 0 või alla eelneva hunger_resistance siis resetib hunger_resistance
            if UniversalVariables.hunger_resistance > hunger_resistance or 0 > UniversalVariables.hunger_resistance:
                return

            UniversalVariables.hunger_resistance = hunger_resistance

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

    #if item == 'Flashlight':
    #    new_player_cone_light_strenght = -70
    #    return new_player_cone_light_strenght

    #grid_y, grid_x = int(UniversalVariables.player_y // UniversalVariables.block_size), int(UniversalVariables.player_x // UniversalVariables.block_size)




#        if UniversalVariables.current_equipped_item == 'Glowstick':
#            self.terrain_data[grid_y][grid_x] = 34
#
#        elif UniversalVariables.current_equipped_item == 'String':
#            if UniversalVariables.string_active:
#                # Deactivate string if already active
#                UniversalVariables.string_active = False
#                print("String deactivated.")
#            else:
#                # Activate string
#                UniversalVariables.string_active = True
#                UniversalVariables.string_start_pos = self.player_rect.center
#                print("String activated at position:", UniversalVariables.string_start_pos)
#    else:
#        if UniversalVariables.string_active:
#            # Draw string following the player
#            def draw_string(screen, color, start_pos, end_pos):
#                pygame.draw.line(screen, color, start_pos, end_pos, 2)
#
#            # Current end position of the string is the player's current center
#            current_end_pos = self.player_rect.center
#            draw_string(UniversalVariables.screen, 'black', UniversalVariables.string_start_pos, current_end_pos)
#    
#    self.click_position = ()