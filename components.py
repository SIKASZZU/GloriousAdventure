import pygame
import time

from HUD import HUD_class
from variables import UniversalVariables
from threading import Timer


class HealthComponent:
    def __init__(self, max_health, min_health):
        self.max_health = max_health
        self.min_health = min_health
        self.current_health = max(min_health, min(max_health, max_health))
        self.health_last_update_time = time.time()

    def heal(self, amount):
        self.current_health = min(self.current_health + amount, self.max_health)

    def damage(self, amount):
        self.current_health = max(self.current_health - amount, self.min_health)

    def get_health(self):
        return self.current_health


class StaminaComponent:
    stamina_bar_decay: int = 0

    def __init__(self, max_stamina, min_stamina):
        self.max_stamina = max_stamina
        self.min_stamina = min_stamina
        self.current_stamina = max(min_stamina, min(max_stamina, max_stamina))
        self.stamina_last_update_time = time.time()
        self.timer = 0
        self.timer_regen = 0

    def use_stamina(self, amount):
        self.current_stamina = round(max(self.current_stamina - amount, self.min_stamina), 3)
        self.stamina_last_update_time = time.time()
        self.timer = 0

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

    def get_stamina(self):
        return self.current_stamina

    def stamina_bar_update(self):
        stamina_rect, stamina_bar_border, stamina_bar_bg = HUD_class.stamina_bar(self, HUD_class.half_w)

        if StaminaComponent.stamina_bar_decay == 120:
            stamina_bar_bg = pygame.Rect(0, 0, 0, 0)
            stamina_rect = pygame.Rect(0, 0, 0, 0)
            stamina_bar_border = pygame.Rect(0, 0, 0, 0)

        if player.stamina.current_stamina >= player.stamina.max_stamina:
            StaminaComponent.stamina_bar_decay += 1

        else:
            HUD_class.stamina_bar_size = player.stamina.current_stamina * HUD_class.ratio  # arvutab stamina bari laiuse
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


class AttackComponent:
    def __init__(self, base_attack_speed, min_attack_speed, max_attack_speed):
        self.base_attack_speed = base_attack_speed
        self.current_speed = max(min_attack_speed, min(max_attack_speed, base_attack_speed))


class HungerComponent:
    pass


class HitBoxComponent:
    pass


class Player:
    def __init__(self, max_health, min_health,
                 max_stamina, min_stamina,
                 base_speed, max_speed, min_speed):
        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health)
        self.stamina = StaminaComponent(max_stamina=max_stamina,
                                        min_stamina=min_stamina)
        self.speed = SpeedComponent(base_speed=base_speed,
                                    max_speed=max_speed,
                                    min_speed=min_speed)
        self.current_health = max_health

        # Start the timer for health regeneration
        self.regeneration_timer = Timer(3, self.regenerate_health)
        self.regeneration_timer.start()

    def check_health(self):
        # Check if health is zero or below
        if self.current_health <= 0:
            print("Player dead")
            self.current_health = 0

    def regenerate_health(self):
        # Increase health by 1 if it's not at maximum
        if self.current_health < self.health.max_health and self.current_health != 0:
            self.current_health += 1
        # Restart the timer
        self.regeneration_timer = Timer(3, self.regenerate_health)
        self.regeneration_timer.start()


player = Player(max_health=20, min_health=0, max_stamina=20, min_stamina=0, base_speed=8, max_speed=10, min_speed=1)
