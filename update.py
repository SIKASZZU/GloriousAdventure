import pygame
from inventory import Inventory


class Game_update:

   # Uuendab player datat ja laseb tal liikuda
    def update_player(self) -> None:
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte

        # Teeb uue player x/y, algne x ja y tuleb playeri maailma panekuga (randint)
        new_player_x: int = self.player_x
        new_player_y: int = self.player_y

        if keys[pygame.K_LSHIFT]:
            self.frame_delay = 10  # Adjust running speed
        else:
            self.frame_delay = 7  # Default walking speed

        if keys[pygame.K_a]:
            self.animation_index = 0  # Left animation
        elif keys[pygame.K_d]:
            self.animation_index = 1  # Right animation
        elif keys[pygame.K_w]:
            self.animation_index = 2  # Up animation
        elif keys[pygame.K_s]:
            self.animation_index = 3  # Down animation

        # Diagonaali speedi fiximine
        if keys[pygame.K_a] and keys[pygame.K_w]:
            new_player_x = self.player_x - self.player.speed.current_speed / 1.5
            new_player_y = self.player_y - self.player.speed.current_speed / 1.5
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            new_player_x = self.player_x - self.player.speed.current_speed / 1.5
            new_player_y = self.player_y + self.player.speed.current_speed / 1.5
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            new_player_x = self.player_x + self.player.speed.current_speed / 1.5
            new_player_y = self.player_y - self.player.speed.current_speed / 1.5
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            new_player_x = self.player_x + self.player.speed.current_speed / 1.5
            new_player_y = self.player_y + self.player.speed.current_speed / 1.5

        # Tavaline player speed (Verikaalselt, horisontaalselt)
        elif keys[pygame.K_a]:
            new_player_x = self.player_x - self.player.speed.current_speed
        elif keys[pygame.K_d]:
            new_player_x = self.player_x + self.player.speed.current_speed
        elif keys[pygame.K_w]:
            new_player_y = self.player_y - self.player.speed.current_speed
        elif keys[pygame.K_s]:
            new_player_y = self.player_y + self.player.speed.current_speed

        # Kui seda pole siis player ei liigu mapi peal
        # Uuendab playeri asukohta vastavalt keyboard inputile
        self.player_x: int = new_player_x
        self.player_y: int = new_player_y
        self.player_rect = pygame.Rect(self.player_x, self.player_y, self.block_size * 0.6, self.block_size * 0.75)

        # Kui player seisab (Animationi jaoks - IDLE)
        is_idle = not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_e])

        if is_idle:
            self.frame = self.idle_animation_manager.update_animation(keys, is_idle)
        else:
            self.frame = self.animation_manager.update_animation(keys, is_idle)
        if self.frame is not None: self.sprite_rect = self.screen.blit(self.frame, (self.player_x, self.player_y))


    # Renderib ainuyksi playeri, tema inventory
    def render_player(self) -> None:
        # Muudab playeri asukohta vastavalt kaamera asukohale / paiknemisele
        player_position_adjusted: tuple[int, int] = (self.player_x + self.offset_x, self.player_y + self.offset_y)
        self.screen.blit(self.frame, player_position_adjusted)  # Renderib playeri animatsioni

        # Inventory
        Inventory.call_inventory(self)  # update playeri osa()

        # Draw a red rectangle around the player
        player_rect = pygame.Rect(player_position_adjusted[0], player_position_adjusted[1], 60, 75)
        pygame.draw.rect(self.screen, (255, 0, 0), player_rect, 2)

    # See peaks olema alati kõige peal
    def render(self) -> None:
        if self.render_inv: Inventory.render_inventory(self)  # renderib inventory

        # Renderib stamina-bari
        if self.stamina_bar_decay < 50:
            pygame.draw.rect(self.screen, '#F7F7F6', self.stamina_rect_bg, 0, 7)
            pygame.draw.rect(self.screen, '#4169E1', self.stamina_rect, 0, 7)
            pygame.draw.rect(self.screen, 'black', self.stamina_rect_border, 2, 7)

        # Uuendab displaid ja fps cap 60
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 0, 0))
        self.screen.blit(fps_text, (100, 150))  # Adjust the position as needed

        pygame.display.update()

        # Limit the frame rate to 60 FPS
        self.clock.tick(60)
