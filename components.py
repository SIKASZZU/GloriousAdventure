import pygame
import time

import items
from variables import UniversalVariables
from inventory import Inventory
from audio import Player_audio
from text import Fading_text
from objects import ObjectManagement

class HealthComponent:
    death_exit_timer = 0
    death_start_time = None
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
                HungerComponent.hunger_timer += 100
                UniversalVariables.health_status = True
        
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        
    def heal(self, item):
        if item == 'Bandage':
            self.current_health += 5
            UniversalVariables.health_status = True

        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def check_health(self, hunger=None):
        self.hunger = hunger
        self.health_cooldown_timer += 1
        if self.current_health <= 0:
            HealthComponent.death(self)

        if self.health_cooldown_timer >= 220:
            HealthComponent.regenerate_health(self, hunger)
            self.health_cooldown_timer = 100
        
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def death(self):
        ### TODO: player moement disable.
        if UniversalVariables.debug_mode == True:
            UniversalVariables.ui_elements.append("""Debug mode, not closing the game.""")
        else:
            if HealthComponent.death_start_time is None:
                HealthComponent.death_start_time = time.perf_counter()

            elapsed_time = time.perf_counter() - HealthComponent.death_start_time
            remaining_time = 5 - int(elapsed_time)

            if remaining_time >= 0:
                UniversalVariables.ui_elements[-1] = f" You have died! Exiting game in {remaining_time} sec. "
            else:
                pygame.quit()

    def get_health(self):
        return self.current_health

    def __str__(self):
        if self.hunger is not None:
            if self.hunger <= 12:
                self.hunger = round(self.hunger, 3)
                if self.hunger <= 0:
                    return f"Health: {self.current_health}/{self.max_health}\n     -- Starvation Damage: {HungerComponent.health_timer} ticks"

                else:
                    return f"Health: {self.current_health}/{self.max_health}\n     -- Regenerating Disabled, Too Hungry: {self.hunger}"

            else:
                return f"Health: {self.current_health}/{self.max_health}"

        else:
            return f"Health: {self.current_health}/{self.max_health}"


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
    hunger_timer = 100
    health_timer = 300
    def __init__(self, base_hunger, max_hunger, min_hunger):
        self.base_hunger = base_hunger
        self.max_hunger = max_hunger
        self.min_hunger = min_hunger
        self.current_hunger = max(min_hunger, min(max_hunger, base_hunger))

    def get_hunger(self):
        return (self.current_hunger)

    def decrease_hunger(self):
        hunger_resist   = 1
        hunger_decrease = 0.1
        if UniversalVariables.player_infected == True:
            hunger_resist   = 2
            hunger_decrease = 0.4

        if UniversalVariables.hunger_resistance:
            UniversalVariables.hunger_resistance -= hunger_resist
            if UniversalVariables.hunger_resistance <= 0:
                UniversalVariables.hunger_resistance = None
                HungerComponent.hunger_timer = 100
            return

        elif self.player.hunger.current_hunger <= 0:

            if HungerComponent.health_timer <= 0:
                if self.player.health.current_health > 0:
                    text = "Starving."

                    if text in Fading_text.shown_texts:
                        Fading_text.shown_texts.remove(text)

                    UniversalVariables.ui_elements.append(text)

                self.player.health.damage(0.5)
                HungerComponent.health_timer = 300
            HungerComponent.health_timer -= 1
        else:
            if HungerComponent.hunger_timer <= 0:
                self.player.hunger.current_hunger = max(self.player.hunger.min_hunger, self.player.hunger.current_hunger - hunger_decrease)
                HungerComponent.hunger_timer = 100

            HungerComponent.hunger_timer -= 1
            if HungerComponent.health_timer < 300:
                HungerComponent.health_timer = 300

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

                        ObjectManagement.remove_object_from_inv(UniversalVariables.current_equipped_item)  # v6tab s66dud itemi 2ra
                        UniversalVariables.hunger_resistance = item.get("Hunger_Resistance")
                        Player_audio.eating_audio(self)

    def __str__(self):
        rounded_hunger = round(self.current_hunger, 3)
        if rounded_hunger == self.min_hunger:
            return f"Hunger: {rounded_hunger}/{self.max_hunger}\n     -- Starving"
        else:
            if UniversalVariables.hunger_resistance is not None:
                return f"Hunger: {rounded_hunger}/{self.max_hunger}\n     -- Hunger Resistance: {UniversalVariables.hunger_resistance} ticks"
            else:
                return f"Hunger: {rounded_hunger}/{self.max_hunger}\n       -- Losing Hunger: {HungerComponent.hunger_timer} ticks"


class Player:
    def __init__(self, max_health, min_health,
                 max_stamina, min_stamina,
                 base_speed, max_speed, min_speed,
                 base_hunger, max_hunger, min_hunger

                 ):
        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health)
        self.stamina = StaminaComponent(max_stamina=max_stamina,
                                        min_stamina=min_stamina)
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
        return f"Player stats:\n   {self.health}\n   {self.stamina}\n   {self.speed}\n   {self.hunger}\n   Inventory: {Inventory.inventory}\n"
