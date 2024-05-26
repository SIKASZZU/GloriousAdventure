import pygame
import time

import items
from HUD import HUD_class
from variables import UniversalVariables
from inventory import Inventory


class HealthComponent:
    death_exit_timer = 0

    def __init__(self, max_health, min_health):
        self.max_health = max_health
        self.min_health = min_health
        self.current_health = max(min_health, min(max_health, max_health))
        self.health_cooldown_timer = 0
        self.previous_health = self.current_health
        self.player_dead_flag = False
        self.hunger = None
    def print_health(self):
        """ Print out player's current health. """

        self.current_health = HealthComponent.get_health(self)

        if not self.player_dead_flag and self.current_health <= 0:
            print("Player dead"); self.player_dead_flag = True
        elif self.previous_health != self.current_health:
            print('Player HP:', self.current_health)
            self.previous_health = self.current_health

    def damage(self, amount):
        self.current_health = max(self.current_health - amount, self.min_health)
        self.health_cooldown_timer = 0
        UniversalVariables.health_status = False
        HealthComponent.check_health(self)

    def regenerate_health(self, hunger):
        if self.current_health < self.max_health and self.current_health != 0:
            if hunger >= 12:
                self.current_health += 1
                HungerComponent.timer_for_next_update += 100
                UniversalVariables.health_status = True

    def check_health(self, hunger=None):
        self.hunger = hunger
        self.health_cooldown_timer += 1
        if self.current_health <= 0:
            HealthComponent.death(self)

        if self.health_cooldown_timer >= 220:
            HealthComponent.regenerate_health(self, hunger)
            self.health_cooldown_timer = 100

    def death(self):
        ### TODO: teha, et ei spammiks printi

        print('Player has died')
        UniversalVariables.ui_elements.append(
            """     You have died!"""
            """  Exiting game in 5 sec. """
        )
        ### TODO: player moement disable.
        if UniversalVariables.debug_mode == True:
            print('Debug mode, not closing the game. ')
        else:
            death_timer_limit = 300
            print('Player has died')
            print(f'Closing the game. {HealthComponent.death_exit_timer}/{death_timer_limit}')
            if HealthComponent.death_exit_timer == death_timer_limit:
                pygame.quit()
            else:
                HealthComponent.death_exit_timer += 1

    def get_health(self):
        return self.current_health

    def __str__(self):
        if self.hunger is not None:
            if self.hunger <= 12:
                self.hunger = round(self.hunger, 3)
                return f"Health: {self.current_health}/{self.max_health}, Regenerating Disabled, Too Hungry: {self.hunger}"

            else:
                return f"Health: {self.current_health}/{self.max_health}"

        else:
            return f"Health: {self.current_health}/{self.max_health}"


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

    def __str__(self):
        return f"Stamina: {self.current_stamina}/{self.max_stamina}"


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

    def __str__(self):
        return f"Speed: {self.current_speed}"


class HungerComponent:

    timer_for_next_update = 0
    def __init__(self, base_hunger, max_hunger, min_hunger):
        self.base_hunger = base_hunger
        self.max_hunger = max_hunger
        self.min_hunger = min_hunger
        self.current_hunger = max(min_hunger, min(max_hunger, base_hunger))

    def get_hunger(self):
        return (self.current_hunger)

    def decrease_hunger(self):
        if UniversalVariables.hunger_resistance:
            UniversalVariables.hunger_resistance -= 1
            if UniversalVariables.hunger_resistance <= 0:
                UniversalVariables.hunger_resistance = None
            return

        else:
            if HungerComponent.timer_for_next_update >= 300:
                self.player.hunger.current_hunger = max(self.player.hunger.min_hunger, self.player.hunger.current_hunger - 0.3)
                HungerComponent.timer_for_next_update = 0

            HungerComponent.timer_for_next_update += 1

    def is_click_inside_player_rect(self):
        if self.click_position != ():
            click_within_x = self.player_rect[0] < self.click_position[0] and self.click_position[0] < self.player_rect[0] + self.player_rect[2]
            click_within_y = self.player_rect[1] < self.click_position[1] and self.click_position[1] < self.player_rect[1] + self.player_rect[3]

            if click_within_x and click_within_y:
                return True
        else:
            return False

    def eat(self):
        if UniversalVariables.current_equipped_item is not None:
            if HungerComponent.is_click_inside_player_rect(self):

                for item in items.items_list:
                    if item["Name"] == UniversalVariables.current_equipped_item and item["Type"] == "Food":
                        satisfaction_gain = item.get("Satisfaction_Gain", 0)

                        # Arvutab uue hungeri 'current + söödud itemi Gain'
                        new_hunger = self.player.hunger.current_hunger + satisfaction_gain


                        # Et playeri hunger ei läheks üle maxi ega alla min
                        if new_hunger >= self.player.hunger.max_hunger:
                            self.player.hunger.current_hunger = self.player.hunger.max_hunger

                        elif new_hunger <= self.player.hunger.min_hunger:
                            self.player.hunger.current_hunger = self.player.hunger.min_hunger

                        else:
                            self.player.hunger.current_hunger = new_hunger

                        # Võtab söödud itemini invist ära
                        if Inventory.inventory.get(UniversalVariables.current_equipped_item, 0) > 0:
                            Inventory.inventory[UniversalVariables.current_equipped_item] -= 1

                            # Kustutab söödud itemi ära kui see on < 0
                            if Inventory.inventory[UniversalVariables.current_equipped_item] <= 0:
                                del Inventory.inventory[UniversalVariables.current_equipped_item]
                                UniversalVariables.current_equipped_item = None

                        UniversalVariables.hunger_resistance = item.get("Hunger_Resistance")

                        # Clear click pos
                        self.click_position = ()

    def __str__(self):
        rounded_hunger = round(self.current_hunger, 3)
        if UniversalVariables.hunger_resistance is not None:
            return f"Hunger: {rounded_hunger}/{self.max_hunger}, Hunger Resistance: {UniversalVariables.hunger_resistance} ticks"
        else:
            return f"Hunger: {rounded_hunger}/{self.max_hunger}"


class Player:
    def __init__(self, max_health, min_health,
                 max_stamina, min_stamina,
                 base_speed, max_speed, min_speed,
                 base_hunger, max_hunger, min_hunger

                 ):
        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health)
        self.stamina = StaminaComponent(max_stamina=max_stamina,
                                        min_stamina=min_stamina,
                                        player=self)
        self.speed = SpeedComponent(base_speed=base_speed,
                                    max_speed=max_speed,
                                    min_speed=min_speed)
        self.hunger = HungerComponent(base_hunger=base_hunger,
                                      max_hunger=max_hunger,
                                      min_hunger=min_hunger)

    def apply_knockback(self, dx, dy):
        knockback_force = 35.0  # Knockback strength, 100.0 == 1 block size almost...
        UniversalVariables.player_x += dx * knockback_force
        UniversalVariables.player_y += dy * knockback_force

    def __str__(self):
        return f"Player stats:\n   {self.health},\n   {self.stamina},\n   {self.speed},\n   {self.hunger},\n   Inventory: {Inventory.inventory}\n"
