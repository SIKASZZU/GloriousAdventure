import pygame

class HUD_class:
    def __init__(self, player, image_loader, variables):
        self.player = player
        self.image_loader = image_loader
        self.variables = variables
            
        self.screen_x: int = self.variables.screen_x
        self.screen_y: int = self.variables.screen_y
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))

        self.stamina_bar_decay = 0
        self.half_w = self.screen.get_size()[0] // 2  # pool screeni widthi

    def update(self):
        self.render_HUD()
        self.display_effects_icons(icon_width=self.variables.icon_width, icon_height=self.variables.icon_height)

    def bar_visualization(self):
        half_w = self.half_w
        sr, sb, sbg, swm, shm = self.stamina_bar(half_w)  # stamina_rect, stamina_bar_size_border, stamina_bar_size_bg
        hr, hb, hbg, hwm, hhm = self.health_bar(half_w)  # health_rect, health_bar_size_border, health_bar_size_bg
        fr, fb, fbg, fwm, fhm = self.food_bar(half_w)  # food_rect, food_bar_size_border, food_bar_size_bg
        hyr, hyb, hybg, hywm, hyhm = self.hydration_bar(half_w)  # food_rect, food_bar_size_border, food_bar_size_bg
        return sr, sb, sbg, hr, hb, hbg, fr, fb, fbg, hwm, hhm, fwm, fhm, hyr, hyb, hybg, hywm, hyhm, swm, shm

    def stamina_bar(self, half_w):
        bar_width = 200
        bar_height = 15
        ratio = bar_width // 20
        screen_y = self.screen_y - 75

        if self.player.stamina.current_stamina >= self.player.stamina.max_stamina:
            self.stamina_bar_decay = min(self.stamina_bar_decay + 1, 120)
        else:
            self.stamina_bar_decay = 0

        if self.stamina_bar_decay == 120:
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

        health_rect_bg = pygame.Rect(half_w - health_bar_size_bg - 6, self.screen_y - 50,
                                     health_bar_size_bg, 45)

        health_rect_border = pygame.Rect(half_w - health_bar_size_border - 6, self.screen_y - 50,
                                         health_bar_size_border, 45)

        player_current_health = self.player.health.get_health()  # player current health
        player_max_health = self.player.health.max_health  # player current health

        val = player_current_health / player_max_health

        health_rect = pygame.Rect(half_w - health_bar_size - 4, (self.screen_y - 5) - (45 * val),
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

        food_rect_bg = pygame.Rect(half_w + 6, self.screen_y - 50,
                                   food_bar_size_bg, 45)

        food_rect_border = pygame.Rect(half_w + 6, self.screen_y - 50,
                                       food_bar_size_border, 45)

        player_current_hunger = self.player.hunger.get_hunger()
        player_max_hunger = self.player.hunger.max_hunger

        val = player_current_hunger / player_max_hunger

        food_rect = pygame.Rect(half_w + 8, (self.screen_y - 5) - (45 * val),
                                food_bar_size - 4, 45 * val)

        # Iconi paigutamiseks bari keskkoha leidmine
        food_w_midpoint = food_rect_border[0] + (food_rect_border[2] // 2) - 25
        food_h_midpoint = food_rect_border[1] + (food_rect_border[3] // 2) - 20

        return food_rect, food_rect_border, food_rect_bg, food_w_midpoint, food_h_midpoint

    def hydration_bar(self, half_w):
        hydration_bar_size_bg: int = 50
        hydration_bar_size_border: int = 50
        hydration_bar_size: int = 50

        hydration_rect_bg = pygame.Rect(half_w + 60, self.screen_y - 50,
                                        hydration_bar_size_bg, 45)

        hydration_rect_border = pygame.Rect(half_w + 60, self.screen_y - 50,
                                            hydration_bar_size_border, 45)

        player_current_thirst = self.player.thirst.get_thirst()
        player_max_thirst = self.player.thirst.max_thirst

        val = player_current_thirst / player_max_thirst

        hydration_rect = pygame.Rect(half_w + 62, (self.screen_y - 5) - (45 * val),
                                     hydration_bar_size - 4, 45 * val)

        # Iconi paigutamiseks bari keskkoha leidmine
        hydration_w_midpoint = hydration_rect_border[0] + (hydration_rect_border[2] // 2) - 25
        hydration_h_midpoint = hydration_rect_border[1] + (hydration_rect_border[3] // 2) - 20

        return hydration_rect, hydration_rect_border, hydration_rect_bg, hydration_w_midpoint, hydration_h_midpoint

    def display_effects_icons(self, icon_width=50, icon_height=50):
        effect_blits_sequence = []
        effects = []

        if self.variables.player_bleeding:
            icon_name = "Bleed"
            effects.append(icon_name)

        if self.variables.player_infected:
            icon_name = "Infection"
            effects.append(icon_name)

        if self.variables.player_poisoned:
            icon_name = "Poison"
            effects.append(icon_name)

        if not effects:
            return

        for i, effect_name in enumerate(effects):
            icon = self.image_loader.load_gui_image(effect_name)
            scaled_icon = pygame.transform.scale(icon, (icon_width, icon_height))

            # Arvutab TOP-RIGHT asukoha iga effectile, mis parasjagu playeril on
            screen_width = self.variables.screen_x
            pos = (screen_width - icon_width - 10, 10 + i * (icon_height + 10))  # Margin 10

            effect_blits_sequence.append((scaled_icon, pos))

        self.variables.screen.blits(effect_blits_sequence)

    def render_HUD(self) -> None:
        """ Renderib HUDi (Stamina-, food- ja healthbari, audio). """
        stamina_rect, stamina_bar_border, stamina_bar_bg, \
            health_rect, health_bar_border, health_bar_bg, \
            food_rect, food_bar_border, food_bar_bg, \
            heart_w_midpoint, heart_h_midpoint, food_w_midpoint, food_h_midpoint, \
            hydration_rect, hydration_bar_border, hydration_bar_bg, hydration_w_midpoint,\
            hydration_h_midpoint, stamina_w_midpoint, stamina_h_midpoint = self.bar_visualization()

        @staticmethod
        def draw_bar(screen, bg_color, bar_rect, fg_color, border_rect, border_width=3, border_radius=7):
            """Helper function to draw a bar with a background, foreground, and border."""
            pygame.draw.rect(screen, bg_color, bar_rect, 0, border_radius)
            pygame.draw.rect(screen, fg_color, bar_rect, 0, border_radius)

            color = 'black'
            if bar_rect != stamina_rect:

                # Y coord mille yletamisel muutub v2rv black to red
                critical_point = ((border_rect[1] + border_rect[3]) + border_rect[1]) / 2

                if bar_rect[1] >= critical_point:
                    color = 'red'

            pygame.draw.rect(screen, color, border_rect, border_width, border_radius)

        # Drawing all bars using the helper function
        draw_bar(self.variables.screen, '#FFBB70', stamina_rect, '#FFEC9E', stamina_bar_border)
        draw_bar(self.variables.screen, '#662828', health_rect, '#FF6666', health_bar_border)
        draw_bar(self.variables.screen, '#78684B', food_rect, '#C8AE7D', food_bar_border)
        draw_bar(self.variables.screen, '#273F87', hydration_rect, '#4169E1', hydration_bar_border)

        if self.stamina_bar_decay != 120:  # Muidu pilt spawnib 0,0 kohta. Idk wtf miks.

            # Stamina bari keskele icon (Stamina.png)
            stamina_icon = self.image_loader.load_gui_image("Stamina")
            scaled_stamina_icon = pygame.transform.scale(stamina_icon, (35, 35))
            self.variables.screen.blit(scaled_stamina_icon, (stamina_w_midpoint, stamina_h_midpoint))

        # Health bari keskele icon (Heart.png)
        heart_icon = self.image_loader.load_gui_image("Health")
        scaled_heart_icon = pygame.transform.scale(heart_icon, (50, 50))
        self.variables.screen.blit(scaled_heart_icon, (heart_w_midpoint, heart_h_midpoint))

        # Food bari keskele icon (Food.png)
        food_icon = self.image_loader.load_gui_image("Food")
        scaled_food_icon = pygame.transform.scale(food_icon, (50, 45))
        self.variables.screen.blit(scaled_food_icon, (food_w_midpoint, food_h_midpoint))

        # Hydration bari keskele icon (Hydration.png)
        hydration_icon = self.image_loader.load_gui_image("Hydration")
        scaled_hydration_icon = pygame.transform.scale(hydration_icon, (50, 40))
        self.variables.screen.blit(scaled_hydration_icon, (hydration_w_midpoint, hydration_h_midpoint))

        # Player's audio icons
        audio_icon_position = (800, 715)
        audio_icon = None

        if self.variables.player_sneaking:
            audio_icon = self.image_loader.load_gui_image("sound_low")
        elif self.variables.player_sprinting:
            audio_icon = self.image_loader.load_gui_image("sound_high")
        else:
            audio_icon = self.image_loader.load_gui_image("sound_average")
        audio_icon = pygame.transform.scale(audio_icon, (50, 50))
        self.variables.screen.blit(audio_icon, audio_icon_position)
