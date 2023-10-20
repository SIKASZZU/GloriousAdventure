import pygame
import time
from HUD import HUD_class


class HealthComponent:
    """
    Represents a health component that manages the health of an object.

    Correct usage:
      HealthComponent(max_health, min_health, health_regeneration_rate)
        OBJECT.command(*args, **kwargs)

    'health_regenerate(self):'
      Calculate and apply health regeneration based on elapsed time and the regeneration rate.
      Ensures that the regenerated health is rounded down to the nearest whole number using math.floor.

    'heal(self, amount):'
      Increase the current health by the specified amount, up to the maximum health limit.

    'damage(self, amount):'
      Decrease the current health by the specified amount, down to the minimum health limit.

    'get_health(self):'
      Retrieve the current health value while applying regeneration if needed.

    Args:
      max_health (float): The maximum health value the component can hold.
      min_health (float): The minimum health value the component can have.
      health_regeneration_rate (float): The rate at which health regenerates, in health points per second.
    """

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

      if self.player.stamina.current_stamina >= self.player.stamina.max_stamina:
          StaminaComponent.stamina_bar_decay += 1

      else:
          HUD_class.stamina_bar_size = self.player.stamina.current_stamina * HUD_class.ratio  # arvutab stamina bari laiuse
          stamina_bar_bg = pygame.Rect(HUD_class.half_w - (HUD_class.stamina_bar_size_bg / 2) - 6, self.screen_y - 75,
                                            HUD_class.stamina_bar_size_bg + 12, 15)  # Kui staminat kulub, ss on background taga
          
          stamina_bar_border = pygame.Rect(HUD_class.half_w - (HUD_class.stamina_bar_size_border / 2) - 6, self.screen_y - 75, 
                                                HUD_class.stamina_bar_size_border + 12, 15)  # K6igi stamina baride ymber border
          
          stamina_rect = pygame.Rect(HUD_class.half_w - (HUD_class.stamina_bar_size / 2) - 6, self.screen_y - 75,
                                          HUD_class.stamina_bar_size + 12, 15)


class SpeedComponent:
    """
    Represents a speed component that manages the speed of an object.

    Correct usage:
      SpeedComponent(base_speed, max_speed, min_speed)
        OBJECT.command(*args, **kwargs)

    'set_speed(self, speed):'
      Set the speed of the object to the specified value, within the maximum and minimum speed limits.

    'get_speed(self):'
      Retrieve the current speed value.

    Args:
      base_speed (float): The base speed value of the object.
      max_speed (float): The maximum speed value the object can have.
      min_speed (float): The minimum speed value the object can have.
    """

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
