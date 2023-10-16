import pygame
import math
from inventory import Inventory
from HUD import HUD_class
from stamina import StaminaComponent
from render import Render_Checker
from objects import Object_Management
from sprite import AnimationManager
from sprite import load_sprite_sheets
class Game_update:
    sprite_sheets, animations = load_sprite_sheets([
        'images/Player/Left.png',
        'images/Player/Right.png',
        'images/Player/Up.png',
        'images/Player/Down.png'
    ])

    sprite_sheets_idle, animations_idle = load_sprite_sheets([
        'images/Player/Idle_Left.png',
        'images/Player/Idle_Right.png',
        'images/Player/Idle_Up.png',
        'images/Player/Idle_Down.png'
    ])

    animation_speeds = [10, 10, 10, 10]

    # Teeb idle ja mitte idle animatsioone
    animation_manager = AnimationManager(sprite_sheets, animations, animation_speeds)
    idle_animation_manager = AnimationManager(sprite_sheets_idle, animations_idle,
                                                    animation_speeds)
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
        self.player_rect = pygame.Rect(self.player_x + Render_Checker.player_hitbox_offset_x, self.player_y + Render_Checker.player_hitbox_offset_y, self.player_width, self.player_height)

        # Kui player seisab (Animationi jaoks - IDLE)
        is_idle = not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_e])

        if is_idle:
            self.frame = Game_update.idle_animation_manager.update_animation(keys, is_idle)
        else:
            self.frame = Game_update.animation_manager.update_animation(keys, is_idle)
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
        player_rect = pygame.Rect(player_position_adjusted[0] + Render_Checker.player_hitbox_offset_x, player_position_adjusted[1] + Render_Checker.player_hitbox_offset_y, self.player_width, self.player_height)

        # Kui vajutad "h" siis tulevad hitboxid visuaalselt nähtavale
        if keys[pygame.K_h] and not self.h_pressed:
            self.h_pressed = True
            Object_Management.hitbox_count += 1
        elif not keys[pygame.K_h]:
            self.h_pressed = False

        if (Object_Management.hitbox_count % 2) != 0:
            pygame.draw.rect(self.screen, (255, 0, 0), player_rect, 2)


    def render_hud(self) -> None:
        #sr, sb, sbg, hr, hb, hbg, fr, fb, fbg, hwm, hhm, fwm, fhm = HUD_class.bar_visualization(self)
        stamina_rect, stamina_bar_border, stamina_bar_bg, \
            health_rect, health_bar_border, health_bar_bg, \
            food_rect, food_bar_border, food_bar_bg, \
            heart_w_midpoint, heart_h_midpoint, food_w_midpoint, food_h_midpoint = HUD_class.bar_visualization(self)
        
        # Renderib stamina-bari
        if StaminaComponent.stamina_bar_decay < 50:
            pygame.draw.rect(self.screen, '#F7F7F6', stamina_bar_bg, 0, 7)
            pygame.draw.rect(self.screen, '#4169E1', stamina_rect, 0, 7)
            pygame.draw.rect(self.screen, 'black', stamina_bar_border, 2, 7)

        # Renderib health-bari
        pygame.draw.rect(self.screen, '#F7F7F6', health_bar_bg, 0, 7)
        pygame.draw.rect(self.screen, '#FF6666', health_rect, 0, 7)
        pygame.draw.rect(self.screen, 'black', health_bar_border, 2, 7)
        
        # Renderib food-bari
        pygame.draw.rect(self.screen, '#F7F7F6', food_bar_bg, 0, 7)
        pygame.draw.rect(self.screen, '#C8AE7D', food_rect, 0, 7)
        pygame.draw.rect(self.screen, 'black', food_bar_border, 2, 7)

        # Health bari keskele icon (Heart.png)
        heart_icon = pygame.image.load('images/Heart.png')
        scaled_heart_icon = pygame.transform.scale(heart_icon, (50, 50))
        self.screen.blit(scaled_heart_icon, (heart_w_midpoint, heart_h_midpoint))
        
        # Food bari keskele icon (Food.png)
        food_icon = pygame.image.load('images/Food.png')
        scaled_food_icon = pygame.transform.scale(food_icon, (50, 50))
        self.screen.blit(scaled_food_icon, (food_w_midpoint, food_h_midpoint))

    # See peaks olema alati kõige peal
    def render(self) -> None:
        if Inventory.render_inv: Inventory.render_inventory(self)  # renderib inventory

        hitbox_text = self.font.render("H - Show hitboxes", True, (155, 5, 5))
        self.screen.blit(hitbox_text, (50, 100))  # Adjust the position as needed

        # Uuendab displaid ja fps cap 60
        fps_text = self.font.render(f"{int(self.clock.get_fps())}", True, (0, 0, 0))
        self.screen.blit(fps_text, (5, 5))  # Adjust the position as needed

        pygame.display.update()

        # Limit the frame rate to 60 FPS
        self.clock.tick(60)
