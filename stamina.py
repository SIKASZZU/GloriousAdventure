import pygame
import time
from HUD import HUD_class

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
