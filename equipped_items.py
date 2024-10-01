import random

from variables import UniversalVariables
from objects import ObjectManagement
from audio import Player_audio
import items
from items import search_item_from_items, ConsumableItem
from text import Fading_text


def is_click_inside_player_rect(self):
    if self.click_position != ():
        player_x = self.player_rect[0] + UniversalVariables.offset_x
        player_y = self.player_rect[1] + UniversalVariables.offset_y
        
        click_within_x = player_x < self.click_position[0] and self.click_position[0] < player_x + self.player_rect[2]
        click_within_y = player_y < self.click_position[1] and self.click_position[1] < player_y + self.player_rect[3]
        if click_within_x and click_within_y:
            return True
        else:
            return False
    else:  
        return False


def probably(chance):
    return random.random() < chance

class ItemFunctionality:

    def update(self):
        ItemFunctionality.current_equipped(self)

    def current_equipped(self):
        """ Argument on item, mille funktsiooni kutsutakse. """

        if not is_click_inside_player_rect(self):
            return

        if UniversalVariables.interaction_delay < UniversalVariables.interaction_delay_max:
            if UniversalVariables.debug_mode:
                print(f'Item delay: {UniversalVariables.interaction_delay} < {UniversalVariables.interaction_delay_max} ')
            return

        equiped_item = UniversalVariables.current_equipped_item
        cure = search_item_from_items(type=ConsumableItem, item_name_or_id=equiped_item, target_attribute="cure")
        poisonous = search_item_from_items(type=ConsumableItem, item_name_or_id=equiped_item, target_attribute="poisonous")
        healing_amount = search_item_from_items(type=ConsumableItem, item_name_or_id=equiped_item, target_attribute="healing_amount")
        satisfaction_gain = search_item_from_items(type=ConsumableItem, item_name_or_id=equiped_item, target_attribute="satisfaction_gain")
        thirst_resistance = search_item_from_items(type=ConsumableItem, item_name_or_id=equiped_item, target_attribute="thirst_resistance")
        hunger_resistance = search_item_from_items(type=ConsumableItem, item_name_or_id=equiped_item, target_attribute="hunger_resistance")

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

        if cure:
            UniversalVariables.interaction_delay = 0
            UniversalVariables.serum_active = True  # see funktsionaalsus j2tkub status.py-is
            ObjectManagement.remove_object_from_inv(equiped_item)

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

        if poisonous :
            UniversalVariables.interaction_delay = 0

            if probably(35 / 100):
                UniversalVariables.player_poisoned = True

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

        if healing_amount:
            UniversalVariables.interaction_delay = 0

            player_healed = self.player.health.heal(healing_amount)
            if player_healed:  ObjectManagement.remove_object_from_inv(equiped_item)
            if UniversalVariables.player_bleeding == True:
                if probably(35 / 100):
                    UniversalVariables.player_bleeding = False

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

        if thirst_resistance and satisfaction_gain:
            UniversalVariables.interaction_delay = 0
            ObjectManagement.remove_object_from_inv(equiped_item)  # v6tab joodud itemi 2ra

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

            Player_audio.drinking_audio(self)
            self.click_position = ()

            # Kui thirst_resistance on alla 0 või alla eelneva thirst_resistance siis resetib thirst_resistance
            if UniversalVariables.thirst_resistance > thirst_resistance or 0 > UniversalVariables.thirst_resistance:
                return

            UniversalVariables.thirst_resistance = thirst_resistance

 # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - # - #

        elif hunger_resistance and satisfaction_gain:
            UniversalVariables.interaction_delay = 0
            ObjectManagement.remove_object_from_inv(equiped_item)  # v6tab s66dud itemi 2ra

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

            Player_audio.eating_audio(self)
            self.click_position = ()

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