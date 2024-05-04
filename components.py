import pygame
import time

from HUD import HUD_class
from variables import UniversalVariables


class HealthComponent:

    def __init__(self, max_health, min_health):
        self.max_health = max_health
        self.min_health = min_health
        self.current_health = max(min_health, min(max_health, max_health))
        self.health_cooldown_timer = 0
        self.previous_health = self.current_health

    def print_health(self):
        """ Print out player's current health. """

        if self.current_health <= 0:
            print("Player dead")
        elif self.previous_health != self.current_health:
            print('Player HP:', self.current_health)

    def damage(self, amount):
        self.current_health = max(self.current_health - amount, self.min_health)
        self.health_cooldown_timer = 0
        UniversalVariables.health_status = False
        HealthComponent.check_health(self)

    def regenerate_health(self):
        if self.current_health < self.max_health and self.current_health != 0:
            self.current_health += 1
            UniversalVariables.health_status = True

    def check_health(self):
        self.health_cooldown_timer += 1
        if self.current_health <= 0:
            return
            # Death screen... (restart game option)
        
        if self.health_cooldown_timer >= 220:
            HealthComponent.regenerate_health(self)
            self.health_cooldown_timer = 100

        self.previous_health = self.current_health

    def get_health(self):
        return self.current_health
    

class StaminaComponent:
    stamina_bar_decay: int = 0

    def __init__(self, max_stamina, min_stamina, player):
        self.max_stamina = max_stamina
        self.min_stamina = min_stamina
        self.current_stamina = max(min_stamina, min(max_stamina, max_stamina))
        self.stamina_last_update_time = time.time()
        self.timer = 0
        self.timer_regen = 0
        self.player = player  # Store the Player instance as an attribute


    def use_stamina(self, amount):
        self.current_stamina = round(max(self.current_stamina - amount, self.min_stamina), 3)
        self.stamina_last_update_time = time.time()
        self.timer = 0
        StaminaComponent.stamina_bar_update(self)

    def stamina_regenerate(self, amount):
        if not self.current_stamina >= self.max_stamina:
            self.timer += 1
            if self.timer >= 60:
                self.timer_regen += 1
                if self.timer_regen >= 3:
                    self.current_stamina = round(self.current_stamina + amount, 3)
                    self.timer_regen = 0
                    if self.current_stamina == self.max_stamina:
                        self.timer = 0
        else:
            self.max_stamina = 20
        StaminaComponent.stamina_bar_update(self)

    def get_stamina(self):
        return self.current_stamina

    def stamina_bar_update(self):
        stamina_rect, stamina_bar_border, stamina_bar_bg = HUD_class.stamina_bar(self, HUD_class.half_w)

        if StaminaComponent.stamina_bar_decay == 120:
            stamina_bar_bg = pygame.Rect(0, 0, 0, 0)
            stamina_rect = pygame.Rect(0, 0, 0, 0)
            stamina_bar_border = pygame.Rect(0, 0, 0, 0)

        try:
            if self.player.stamina.current_stamina >= self.player.stamina.max_stamina:
                StaminaComponent.stamina_bar_decay += 1

            else:
                HUD_class.stamina_bar_size = self.player.stamina.current_stamina * HUD_class.ratio  # arvutab stamina bari laiuse
                stamina_bar_bg = pygame.Rect(HUD_class.half_w - (HUD_class.stamina_bar_size_bg / 2) - 6,
                                            UniversalVariables.screen_y - 75,
                                            HUD_class.stamina_bar_size_bg + 12,
                                            15)  # Kui staminat kulub, ss on background taga

                stamina_bar_border = pygame.Rect(HUD_class.half_w - (HUD_class.stamina_bar_size_border / 2) - 6,
                                                UniversalVariables.screen_y - 75,
                                                HUD_class.stamina_bar_size_border + 12,
                                                15)  # K6igi stamina baride ymber border

                stamina_rect = pygame.Rect(HUD_class.half_w - (HUD_class.stamina_bar_size / 2) - 6,
                                        UniversalVariables.screen_y - 75,
                                        HUD_class.stamina_bar_size + 12, 15)
        except AttributeError as ae: print('Error @ components.py', ae)

class SpeedComponent:
    def __init__(self, base_speed, max_speed, min_speed):
        self.base_speed = base_speed
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.current_speed = max(min_speed, min(max_speed, base_speed))

    def set_speed(self, speed):
        self.current_speed = max(min(speed, self.max_speed), self.min_speed)
        return self.current_speed  # Return the newly set speed value

    def get_speed(self):
        return self.current_speed


class Player:
    def __init__(self, max_health, min_health,
                 max_stamina, min_stamina,
                 base_speed, max_speed, min_speed):
        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health)
        self.stamina = StaminaComponent(max_stamina=max_stamina,
                                        min_stamina=min_stamina,
                                        player=self)
        self.speed = SpeedComponent(base_speed=base_speed,
                                    max_speed=max_speed,
                                    min_speed=min_speed)
