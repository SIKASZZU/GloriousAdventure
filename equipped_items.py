import pygame
from variables import UniversalVariables


def is_click_inside_player_rect(self):
        if self.click_position != ():
            print(self.player_rect, self.click_position)
            click_within_x = self.player_rect[0] < self.click_position[0] and self.click_position[0] < self.player_rect[0] + self.player_rect[2]
            click_within_y = self.player_rect[1] < self.click_position[1] and self.click_position[1] < self.player_rect[1] + self.player_rect[3]
            print(click_within_x, click_within_y)
            if click_within_x and click_within_y:
                return True
            else:
                return False
        else:  
            return False

def current_equipped(self):
    """ Argument on item, mille funktsiooni kutsutakse. """

    #if item == 'Flashlight':
    #    new_player_cone_light_strenght = -70
    #    return new_player_cone_light_strenght

    #if item == 'Bread': ...
    #print('calling func')
    grid_y, grid_x = int(UniversalVariables.player_y // UniversalVariables.block_size), int(UniversalVariables.player_x // UniversalVariables.block_size)

    if is_click_inside_player_rect(self):
        if UniversalVariables.current_equipped_item == 'Glowstick':
            self.terrain_data[grid_y][grid_x] = 34

        elif UniversalVariables.current_equipped_item == 'String':
            if UniversalVariables.string_active:
                # Deactivate string if already active
                UniversalVariables.string_active = False
                print("String deactivated.")
            else:
                # Activate string
                UniversalVariables.string_active = True
                UniversalVariables.string_start_pos = self.player_rect.center
                print("String activated at position:", UniversalVariables.string_start_pos)
    else:
        if UniversalVariables.string_active:
            # Draw string following the player
            def draw_string(screen, color, start_pos, end_pos):
                pygame.draw.line(screen, color, start_pos, end_pos, 2)

            # Current end position of the string is the player's current center
            current_end_pos = self.player_rect.center
            draw_string(UniversalVariables.screen, 'black', UniversalVariables.string_start_pos, current_end_pos)
    
    self.click_position = ()