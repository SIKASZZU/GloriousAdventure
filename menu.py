import pygame
import sys

from variables import UniversalVariables
from images import menu_images
from button import Button

class Menu():

    screen_x = UniversalVariables.screen_x

    resume_button = Button(screen_x / 2 - 100, 175, menu_images["resume_img"], 1)
    options_button = Button(screen_x / 2 - 106, 300, menu_images["options_img"], 1)
    video_button = Button(screen_x / 2 - 178, 125, menu_images["video_img"], 1)
    audio_button = Button(screen_x / 2 - 179, 250, menu_images["audio_img"], 1)
    keys_button = Button(screen_x / 2 - 159, 375, menu_images["keys_img"], 1)
    back_button = Button(screen_x / 2 - 72, 500, menu_images["back_img"], 1)
    quit_button = Button(screen_x / 2 - 69, 425, menu_images["quit_img"], 1)

    def settings_menu(self):
        if self.menu_state == "main":
            # draw pause screen buttons
            if Menu.resume_button.draw(self.screen):
                self.game_paused = False
            if Menu.options_button.draw(self.screen):
                self.menu_state = "options"
            if Menu.quit_button.draw(self.screen):
                pygame.quit()
                sys.exit()

        # check if the options menu is open
        if self.menu_state == "options":
            # draw the different options buttons
            if Menu.video_button.draw(self.screen):
                print("Video Settings")
            if Menu.audio_button.draw(self.screen):
                print("Audio Settings")
            if Menu.keys_button.draw(self.screen):
                print("Change Key Bindings")
            if Menu.back_button.draw(self.screen):
                self.menu_state = "main"