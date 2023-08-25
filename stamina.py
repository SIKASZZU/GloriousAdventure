import pygame
from game_entities import Player



def stamina_bar_update(self):
        
    # Functiooni algus
    if self.stamina_bar_decay == 120:
        self.stamina_rect_bg = pygame.Rect(0, 0, 0, 0)
        self.stamina_rect = pygame.Rect(0, 0, 0, 0)
        self.stamina_rect_border = pygame.Rect(0, 0, 0, 0)
        
    if self.player.stamina.current_stamina >= self.player.stamina.max_stamina:
        self.stamina_bar_decay += 1

    else:
        self.stamina_bar_size = self.player.stamina.current_stamina * self.ratio  # arvutab stamina bari laiuse
        self.stamina_rect_bg = pygame.Rect(self.half_w - (self.stamina_bar_size_bg / 2) - 6, self.screen_y - 25, self.stamina_bar_size_bg + 12, 15)  # Kui staminat kulub, ss on background taga
        self.stamina_rect_border = pygame.Rect(self.half_w - (self.stamina_bar_size_border / 2) - 6, self.screen_y - 25, self.stamina_bar_size_border + 12, 15)  # K6igi stamina baride ymber border
        self.stamina_rect = pygame.Rect(self.half_w - (self.stamina_bar_size / 2) - 6, self.screen_y - 25, self.stamina_bar_size + 12, 15)
