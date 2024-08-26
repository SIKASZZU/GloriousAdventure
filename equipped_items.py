import random

from variables import UniversalVariables
from objects import ObjectManagement
from audio import Player_audio
import items


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

        if is_click_inside_player_rect(self):

            if UniversalVariables.item_delay < UniversalVariables.item_delay_max:
                return print(f'Item delay: {UniversalVariables.item_delay} < 70 ')

            equiped_item = UniversalVariables.current_equipped_item


            # ITEMS
            if equiped_item == 'Bandage':
                player_healed = self.player.health.heal(equiped_item)
                if player_healed:  ObjectManagement.remove_object_from_inv(equiped_item)
                if UniversalVariables.player_bleeding == True:
                    if probably(35 / 100):
                        UniversalVariables.player_bleeding = False
                
            if equiped_item == 'Serum':
                UniversalVariables.serum_active = True  # see funktsionaalsus j2tkub status.py-is
                ObjectManagement.remove_object_from_inv(equiped_item)

            if equiped_item in ['Сanteen', 'Bottle_Water']:
                print('Canteen = no functionality yet')
                ### TODO: fix code repetition!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! FUNCTIOOONS FUNCTIOOOOOOOOONS
                ### TODO: Bottle Wateril võiks olla 3 võimalust kasutada vmdgi

                for item in items.items_list:
                    if item["Name"] == equiped_item and item["Type"] == "Food":
                        satisfaction_gain = item.get("Satisfaction_Gain", 0)

                        # Arvutab uue thirsti 'current + söödud itemi Gain'
                        new_thirst = self.player.thirst.current_thirst + satisfaction_gain

                        # Et playeri thirst ei läheks üle maxi ega alla min
                        if new_thirst >= self.player.thirst.max_thirst:
                            self.player.thirst.current_thirst = self.player.thirst.max_thirst

                        elif new_thirst <= self.player.thirst.min_thirst:
                            self.player.thirst.current_thirst = self.player.thirst.min_thirst

                        else:
                            self.player.thirst.current_thirst = new_thirst

                        UniversalVariables.hunger_resistance = item.get("Thirst_Resistance")
                        ObjectManagement.remove_object_from_inv(equiped_item)  # v6tab s66dud itemi 2ra
                        Player_audio.drinking_audio(self)
                        self.click_position = ()

            if equiped_item in ['Bread', 'Meat']:
                for item in items.items_list:
                    if item["Name"] == equiped_item and item["Type"] == "Food":
                        satisfaction_gain = item.get("Satisfaction_Gain", 0)

                        # Arvutab uue hungeri 'current + söödud itemi Gain'
                        new_hunger = self.player.hunger.current_hunger + satisfaction_gain

                        # Et playeri hunger ei läheks üle maxi ega alla min
                        if new_hunger >= self.player.hunger.max_hunger:
                            self.player.hunger.current_hunger = self.player.hunger.max_hunger

                        elif new_hunger <= self.player.hunger.min_hunger:
                            self.player.hunger.current_hunger = self.player.hunger.min_hunger

                        else:
                            self.player.hunger.current_hunger = new_hunger

                        UniversalVariables.hunger_resistance = item.get("Hunger_Resistance")
                        ObjectManagement.remove_object_from_inv(equiped_item)  # v6tab s66dud itemi 2ra
                        Player_audio.eating_audio(self)
                        self.click_position = ()
            UniversalVariables.item_delay = 0

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