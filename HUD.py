import pygame
from variables import UniversalVariables

class HUD_class:
    
    # need v6iks nahhuj siit saada. Game classi ei saa importida - circular porno
    screen_x: int = UniversalVariables.screen_x
    screen_y: int = UniversalVariables.screen_y
    screen = pygame.display.set_mode((screen_x, screen_y))

    stamina_bar_decay = 0
    half_w = screen.get_size()[0] // 2  # pool screeni widthi

    def bar_visualization(self):
        half_w = HUD_class.half_w
        sr, sb, sbg = HUD_class.stamina_bar(self, half_w)  # stamina_rect, stamina_bar_size_border, stamina_bar_size_bg
        hr, hb, hbg, hwm, hhm = HUD_class.health_bar(self, half_w)  # health_rect, health_bar_size_border, health_bar_size_bg
        fr, fb, fbg, fwm, fhm = HUD_class.food_bar(self, half_w)  # food_rect, food_bar_size_border, food_bar_size_bg
        
        return sr, sb, sbg, hr, hb, hbg, fr, fb, fbg, hwm, hhm, fwm, fhm,
    
    
    def stamina_bar(self, half_w):
        stamina_bar_size: int = 200
        stamina_bar_size_bg: int = 200
        stamina_bar_size_border: int = 200
        ratio = stamina_bar_size // 20  # Stamina bari suuruse muutmiseks

        if self.player.stamina.current_stamina >= self.player.stamina.max_stamina and HUD_class.stamina_bar_decay != 120:
            HUD_class.stamina_bar_decay += 1
        
        if HUD_class.stamina_bar_decay == 120:
            stamina_rect_bg = pygame.Rect(0, 0, 0, 0)
            stamina_rect_border = pygame.Rect(0, 0, 0, 0)
            stamina_rect = pygame.Rect(0, 0, 0, 0)
        
        else:
            stamina_bar_size = self.player.stamina.current_stamina * ratio  # arvutab stamina bari laiuse

            stamina_rect_bg = pygame.Rect(half_w - (stamina_bar_size_bg / 2) - 6, HUD_class.screen_y - 75,
                                                stamina_bar_size_bg + 12, 15)  # Kui staminat kulub, ss on background taga
            
            stamina_rect_border = pygame.Rect(half_w - (stamina_bar_size_border / 2) - 6, HUD_class.screen_y - 75,
                                                    stamina_bar_size_border + 12, 15)  # K6igi stamina baride ymber border
            
            stamina_rect = pygame.Rect(half_w - (stamina_bar_size / 2) - 6, HUD_class.screen_y - 75,
                                            stamina_bar_size + 12, 15)
            
        return stamina_rect, stamina_rect_border, stamina_rect_bg


    def health_bar(self, half_w):    
        health_bar_size_bg: int = 100
        health_bar_size_border: int = 100
        health_bar_size: int = 100

        health_rect_bg = pygame.Rect(half_w - health_bar_size_bg - 6, HUD_class.screen_y - 50,
                                            health_bar_size_bg, 45)
        
        health_rect_border = pygame.Rect(half_w - health_bar_size_border - 6, HUD_class.screen_y - 50,
                                                health_bar_size_border, 45)
        
        player_current_health =  self.player.health.get_health()  # player current health
        player_max_health = self.player.health.max_health  # player current health

        val = player_current_health / player_max_health

        health_rect = pygame.Rect(half_w - health_bar_size - 4, (HUD_class.screen_y - 5) - (45 * val),
                                        health_bar_size - 4, 45 * val)

        # Iconi paigutamiseks bari keskkoha leidmine
        heart_w_midpoint = health_rect_border[0] + (health_rect_border[2] // 2) - 25  # -25 sest, me suurendame pilti 50px võrra ning muidu ei jää pilt keskele.
        heart_h_midpoint = health_rect_border[1] + (health_rect_border[3] // 2) - 25
        
        return health_rect, health_rect_border, health_rect_bg, heart_w_midpoint, heart_h_midpoint
    

    def food_bar(self, half_w):
        food_bar_size_bg: int = 100
        food_bar_size_border: int = 100
        food_bar_size: int = 100

        food_rect_bg = pygame.Rect(half_w + 6, HUD_class.screen_y - 50,
                                            food_bar_size_bg, 45)
        
        food_rect_border = pygame.Rect(half_w + 6, HUD_class.screen_y - 50,
                                                food_bar_size_border, 45)

        player_current_hunger = self.player.hunger.get_hunger()
        player_max_hunger = self.player.hunger.max_hunger

        val = player_current_hunger / player_max_hunger
            
        food_rect = pygame.Rect(half_w + 8, (HUD_class.screen_y - 5) - (45 * val),
                                        food_bar_size - 4, 45 * val)
        
        # Iconi paigutamiseks bari keskkoha leidmine
        food_w_midpoint = food_rect_border[0] + (food_rect_border[2] // 2) - 25
        food_h_midpoint = food_rect_border[1] + (food_rect_border[3] // 2) - 20

        return food_rect, food_rect_border, food_rect_bg, food_w_midpoint, food_h_midpoint