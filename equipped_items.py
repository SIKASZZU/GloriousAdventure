import random

from variables import UniversalVariables
from objects import ObjectManagement


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

            item_at_hand = UniversalVariables.current_equipped_item

            # ITEMS
            if item_at_hand == 'Bandage':
                if UniversalVariables.player_bleeding == True:
                    self.player.health.heal(item_at_hand)
                    ObjectManagement.remove_object_from_inv(item_at_hand)
                    
                    if probably(35 / 100):
                        UniversalVariables.player_bleeding = False

            if item_at_hand == 'Serum':
                UniversalVariables.serum_active = True  # see funktsionaalsus j2tkub status.py-is
                ObjectManagement.remove_object_from_inv(item_at_hand)

            if UniversalVariables.current_equipped_item == 'Сanteen':
                ...


    #if item == 'Flashlight':
    #    new_player_cone_light_strenght = -70
    #    return new_player_cone_light_strenght

    #if item == 'Bread': ...
    #print('calling func')


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