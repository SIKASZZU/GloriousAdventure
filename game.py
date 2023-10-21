# Pythoni inbuilt/downloaded files
import pygame
import sys

# Oma enda failid
from camera import Camera  # box_target_camera
from inventory import Inventory
from update import PlayerUpdate  # update_player, render_player
from render import RenderPictures  # map_render
from collisions import Collisions  # check_collisions, collison_terrain, collision_hitbox
from objects import ObjectManagement
from render import CreateCollisionBoxes  # object_list_creation
from components import StaminaComponent

from variables import UniversalVariables
from images import menu_images
from button import Button


class Game:
    pygame.init()
    pygame.display.set_caption("Glorious Adventure - BETA")

    # ******************** PLAYER ******************** #
    player_rect = None  # seda ei pea olema, aga mdea, suht perses. Code settib r2igelt self argumente, mida ei eksisteeri

    # ******************** FPS, FONT ******************** #
    clock = pygame.time.Clock()  # fps
    font = pygame.font.SysFont("Verdana", 20)  # font

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_paused = True
                if event.key == pygame.K_SPACE:
                    self.game_paused = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    font = pygame.font.SysFont("Verdana", 20)  # font
    # ******************** Menu ******************** #
    screen_x = UniversalVariables.screen_x
    screen = UniversalVariables.screen
    menu_state = "main"
    game_paused = False

    resume_button = Button(screen_x / 2 - 100, 175, menu_images["resume_img"], 1)
    options_button = Button(screen_x / 2 - 106, 300, menu_images["options_img"], 1)
    quit_button = Button(screen_x / 2 - 69, 425, menu_images["quit_img"], 1)

    video_button = Button(screen_x / 2 - 178, 125, menu_images["video_img"], 1)
    audio_button = Button(screen_x / 2 - 179, 250, menu_images["audio_img"], 1)
    keys_button = Button(screen_x / 2 - 159, 375, menu_images["keys_img"], 1)
    back_button = Button(screen_x / 2 - 72, 500, menu_images["back_img"], 1)

    def run(self) -> None:
        while True:
            self.screen.fill((0, 50, 0))  # Fill with a background color (black in this case)
            #print(UniversalVariables.terrain_data)
            self.handle_events()  # Paneb mängu õigesti kinni

            # Vaatab kas mäng on pausi peale pandud või mitte
            # check if game is paused
            if self.game_paused == True:
                # check menu state
                if self.menu_state == "main":
                    # draw pause screen buttons
                    if self.resume_button.draw(self.screen):
                        self.game_paused = False
                    if self.options_button.draw(self.screen):
                        self.menu_state = "options"
                    if self. quit_button.draw(self.screen):
                        pygame.quit()
                        sys.exit()
                # check if the options menu is open
                if self.menu_state == "options":
                    # draw the different options buttons
                    if self.video_button.draw(self.screen):
                        print("Video Settings")
                    if self.audio_button.draw(self.screen):
                        print("Audio Settings")
                    if self.keys_button.draw(self.screen):
                        print("Change Key Bindings")
                    if self.back_button.draw(self.screen):
                        self.menu_state = "main"

                pygame.display.update()

            else:
                self.handle_events()  # Paneb mängu õigesti kinni
                PlayerUpdate.update_player(self)  # Uuendab mängija asukohta, ja muid asju
                Camera.box_target_camera(self)  # Kaamera


                StaminaComponent.stamina_bar_update(self)  # Stamina bar

                # collision things
                Collisions.collison_terrain(self)
                Collisions.check_collisions(self)  # Vaatab mängija kokkup6rkeid objecktidega

                CreateCollisionBoxes.object_list_creation(self)  # Creatib UniversalVariables.collision_boxes
                RenderPictures.map_render(self)  # Renderib terraini

                if Collisions.render_after == True:  # Renderib objectid peale playerit. Illusioon et player on objecti taga.
                    ObjectManagement.place_and_render_object(self)  # Renderib objektid
                    PlayerUpdate.render_player(self)  # Renderib playeri (+ tema recti)
                else:  # self.render_after == False
                    PlayerUpdate.render_player(self)
                    ObjectManagement.place_and_render_object(self)  # Renderib objektid

                Inventory.handle_mouse_click(self)  # Inventorisse clickimise systeem
                PlayerUpdate.render_HUD(self)  # Render HUD_class (health- ,food- ,stamina bar)
                PlayerUpdate.render_general(self)  # inventory, fps counteri

if __name__ == "__main__":
    game = Game()
    game.run()
