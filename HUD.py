import pygame
from variables import UniversalVariables
from images import ImageLoader


class HUD_class:
    # need v6iks nahhuj siit saada. Game classi ei saa importida - circular porno
    screen_x: int = UniversalVariables.screen_x
    screen_y: int = UniversalVariables.screen_y
    screen = pygame.display.set_mode((screen_x, screen_y))

    stamina_bar_decay = 0
    half_w = screen.get_size()[0] // 2  # pool screeni widthi

    @staticmethod
    def update():
        HUD_class.display_effects_icons(icon_width=UniversalVariables.icon_width, icon_height=UniversalVariables.icon_height)

    def bar_visualization(self):
        half_w = HUD_class.half_w
        sr, sb, sbg, swm, shm = HUD_class.stamina_bar(self,
                                                      half_w)  # stamina_rect, stamina_bar_size_border, stamina_bar_size_bg
        hr, hb, hbg, hwm, hhm = HUD_class.health_bar(self,
                                                     half_w)  # health_rect, health_bar_size_border, health_bar_size_bg
        fr, fb, fbg, fwm, fhm = HUD_class.food_bar(self, half_w)  # food_rect, food_bar_size_border, food_bar_size_bg
        hyr, hyb, hybg, hywm, hyhm = HUD_class.hydration_bar(self,
                                                             half_w)  # food_rect, food_bar_size_border, food_bar_size_bg
        return sr, sb, sbg, hr, hb, hbg, fr, fb, fbg, hwm, hhm, fwm, fhm, hyr, hyb, hybg, hywm, hyhm, swm, shm

    def stamina_bar(self, half_w):
        bar_width = 200
        bar_height = 15
        ratio = bar_width // 20
        screen_y = HUD_class.screen_y - 75

        if self.player.stamina.current_stamina >= self.player.stamina.max_stamina:
            HUD_class.stamina_bar_decay = min(HUD_class.stamina_bar_decay + 1, 120)
        else:
            HUD_class.stamina_bar_decay = 0

        if HUD_class.stamina_bar_decay == 120:
            return pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0), 0, 0

        current_stamina_width = self.player.stamina.current_stamina * ratio
        center_x = half_w - 6

        # Create rectangles for the stamina bar
        stamina_rect_bg = pygame.Rect(center_x - (bar_width // 2), screen_y, bar_width + 12, bar_height)
        stamina_rect_border = pygame.Rect(center_x - (bar_width // 2), screen_y, bar_width + 12, bar_height)
        stamina_rect = pygame.Rect(center_x - (current_stamina_width // 2), screen_y, current_stamina_width + 12,
                                   bar_height)

        # Calculate midpoints for positioning
        stamina_width_midpoint = stamina_rect_border.centerx - 18
        stamina_height_midpoint = stamina_rect_border.centery - 15

        return stamina_rect, stamina_rect_border, stamina_rect_bg, stamina_width_midpoint, stamina_height_midpoint

    def health_bar(self, half_w):
        health_bar_size_bg: int = 100
        health_bar_size_border: int = 100
        health_bar_size: int = 100

        health_rect_bg = pygame.Rect(half_w - health_bar_size_bg - 6, HUD_class.screen_y - 50,
                                     health_bar_size_bg, 45)

        health_rect_border = pygame.Rect(half_w - health_bar_size_border - 6, HUD_class.screen_y - 50,
                                         health_bar_size_border, 45)

        player_current_health = self.player.health.get_health()  # player current health
        player_max_health = self.player.health.max_health  # player current health

        val = player_current_health / player_max_health

        health_rect = pygame.Rect(half_w - health_bar_size - 4, (HUD_class.screen_y - 5) - (45 * val),
                                  health_bar_size - 4, 45 * val)

        # Iconi paigutamiseks bari keskkoha leidmine
        heart_w_midpoint = health_rect_border[0] + (health_rect_border[
                                                        2] // 2) - 25  # -25 sest, me suurendame pilti 50px võrra ning muidu ei jää pilt keskele.
        heart_h_midpoint = health_rect_border[1] + (health_rect_border[3] // 2) - 25
        return health_rect, health_rect_border, health_rect_bg, heart_w_midpoint, heart_h_midpoint

    def food_bar(self, half_w):
        food_bar_size_bg: int = 50
        food_bar_size_border: int = 50
        food_bar_size: int = 50

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

    def hydration_bar(self, half_w):
        hydration_bar_size_bg: int = 50
        hydration_bar_size_border: int = 50
        hydration_bar_size: int = 50

        hydration_rect_bg = pygame.Rect(half_w + 60, HUD_class.screen_y - 50,
                                        hydration_bar_size_bg, 45)

        hydration_rect_border = pygame.Rect(half_w + 60, HUD_class.screen_y - 50,
                                            hydration_bar_size_border, 45)

        player_current_thirst = self.player.thirst.get_thirst()
        player_max_thirst = self.player.thirst.max_thirst

        val = player_current_thirst / player_max_thirst

        hydration_rect = pygame.Rect(half_w + 62, (HUD_class.screen_y - 5) - (45 * val),
                                     hydration_bar_size - 4, 45 * val)

        # Iconi paigutamiseks bari keskkoha leidmine
        hydration_w_midpoint = hydration_rect_border[0] + (hydration_rect_border[2] // 2) - 25
        hydration_h_midpoint = hydration_rect_border[1] + (hydration_rect_border[3] // 2) - 20

        return hydration_rect, hydration_rect_border, hydration_rect_bg, hydration_w_midpoint, hydration_h_midpoint

    @staticmethod
    def display_effects_icons(icon_width=50, icon_height=50):
        effect_blits_sequence = []
        effects = []

        if UniversalVariables.player_bleeding:
            icon_name = "Bleed"
            effects.append(icon_name)

        if UniversalVariables.player_infected:
            icon_name = "Infection"
            effects.append(icon_name)

        if UniversalVariables.player_poisoned:
            icon_name = "Poison"
            effects.append(icon_name)

        if not effects:
            return

        for i, effect_name in enumerate(effects):
            icon = ImageLoader.load_gui_image(effect_name)
            scaled_icon = pygame.transform.scale(icon, (icon_width, icon_height))

            # Arvutab TOP-RIGHT asukoha iga effectile, mis parasjagu playeril on
            screen_width = UniversalVariables.screen_x
            pos = (screen_width - icon_width - 10, 10 + i * (icon_height + 10))  # Margin 10

            effect_blits_sequence.append((scaled_icon, pos))

        UniversalVariables.screen.blits(effect_blits_sequence)


