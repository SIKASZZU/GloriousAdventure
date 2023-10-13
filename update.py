import pygame
import math
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

        if keys[pygame.K_d]:
            self.animation_index = 1  # Right animation
        elif keys[pygame.K_a]:
            self.animation_index = 0  # Left animation
        elif keys[pygame.K_s]:
            self.animation_index = 3  # Down animation
        elif keys[pygame.K_w]:
            self.animation_index = 2  # Up animation

        x = -1 * int(keys[pygame.K_a]) + 1 * int(keys[pygame.K_d])
        y = -1 * int(keys[pygame.K_w]) + 1 * int(keys[pygame.K_s])

        magnitude = math.sqrt(x ** 2 + y ** 2)
        if magnitude == 0:
            normalized_x, normalized_y = 0, 0  # Avoid division by zero
        else:
            normalized_x = x / magnitude
            normalized_y = y / magnitude

        new_player_x = self.player_x + self.player.speed.current_speed * normalized_x
        new_player_y = self.player_y + self.player.speed.current_speed * normalized_y

        # Kui seda pole siis player ei liigu mapi peal
        # Uuendab playeri asukohta vastavalt keyboard inputile
        self.player_x: int = new_player_x
        self.player_y: int = new_player_y
        self.player_rect = pygame.Rect(self.player_x + self.player_hitbox_offset_x, self.player_y + self.player_hitbox_offset_y, self.player_width, self.player_height)

        # Kui player seisab (Animationi jaoks - IDLE)
        is_idle = not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_e])

        if is_idle:
            self.frame = self.idle_animation_manager.update_animation(keys, is_idle)
        else:
            self.frame = self.animation_manager.update_animation(keys, is_idle)
        if self.frame is not None: self.sprite_rect = self.screen.blit(self.frame, (self.player_x, self.player_y))


    # Renderib ainuyksi playeri, tema inventory
    def render_player(self) -> None:
        keys = pygame.key.get_pressed()

        # Muudab playeri asukohta vastavalt kaamera asukohale / paiknemisele
        player_position_adjusted: tuple[int, int] = (self.player_x + self.offset_x, self.player_y + self.offset_y)
        self.screen.blit(self.frame, player_position_adjusted)  # Renderib playeri animatsioni

        # Inventory
        Inventory.call_inventory(self)  # update playeri osa()

        # Joonistab playeri ümber punase ringi ehk playeri hitboxi
        player_rect = pygame.Rect(player_position_adjusted[0] + self.player_hitbox_offset_x, player_position_adjusted[1] + self.player_hitbox_offset_y, self.player_width, self.player_height)

        # Kui vajutad "h" siis tulevad hitboxid visuaalselt nähtavale
        if keys[pygame.K_h] and not self.h_pressed:
            self.h_pressed = True
            self.hitbox_count += 1
        elif not keys[pygame.K_h]:
            self.h_pressed = False

        if (self.hitbox_count % 2) != 0:
            pygame.draw.rect(self.screen, (255, 0, 0), player_rect, 2)

    # See peaks olema alati kõige peal
    def render(self) -> None:
        if self.render_inv: Inventory.render_inventory(self)  # renderib inventory

        # Renderib stamina-bari
        if self.stamina_bar_decay < 50:
            pygame.draw.rect(self.screen, '#F7F7F6', self.stamina_rect_bg, 0, 7)
            pygame.draw.rect(self.screen, '#4169E1', self.stamina_rect, 0, 7)
            pygame.draw.rect(self.screen, 'black', self.stamina_rect_border, 2, 7)

        # Renderib health-bari
        pygame.draw.rect(self.screen, '#F7F7F6', self.health_rect_bg, 0, 7)
        pygame.draw.rect(self.screen, '#FF6666', self.health_rect, 0, 7)
        pygame.draw.rect(self.screen, 'black', self.health_rect_border, 2, 7)


        hitbox_text = self.font.render("H - Show hitboxes", True, (155, 5, 5))
        self.screen.blit(hitbox_text, (50, 100))  # Adjust the position as needed

        # Uuendab displaid ja fps cap 60
        fps_text = self.font.render(f"{int(self.clock.get_fps())}", True, (0, 0, 0))
        self.screen.blit(fps_text, (5, 5))  # Adjust the position as needed

        pygame.display.update()

        # Limit the frame rate to 60 FPS
        self.clock.tick(60)
