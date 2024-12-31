import pygame
import time

from variables import UniversalVariables
from inventory import Inventory

class HealthComponent:
    def __init__(self, max_health, min_health, fading_text):
        self.fading_text = fading_text
        self.death_start_time = None
        self.max_health = max_health
        self.min_health = min_health
        self.current_health = max(min_health, min(max_health, max_health))
        self.health_cooldown_timer = 0
        self.previous_health = self.current_health
        self.player_dead_flag = False
        self.health_timer = 150

    def update(self, hunger_cls_import):
        self.hunger = hunger_cls_import

        current_hunger = self.hunger.current_hunger
        self.check_health(current_hunger)


    def print_health(self):
        """ Print out player's current health. """

        self.current_health = self.get_health()

        if not self.player_dead_flag and self.current_health <= 0:
            print("Player dead"); self.player_dead_flag = True
        elif self.previous_health != self.current_health:
            print('Player HP:', self.current_health)
            self.previous_health = self.current_health

    def damage(self, amount):
        self.current_health = max(self.current_health - amount, self.min_health)
        self.health_cooldown_timer = 0
        self.variables.health_status = False
        self.check_health()

    def regenerate_health(self, hunger):
        if self.current_health < self.max_health and self.current_health != 0:
            if hunger >= 12:
                self.current_health += 1
                self.hunger.hunger_timer += 100
                self.variables.health_status = True
        
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        
    def heal(self, amount):
        # et player ei overhealiks ennast. Health cap on ikkagi olemas.
        if self.current_health == self.max_health:
            self.fading_text.re_display_fading_text(f'Max health reached!')
            return False  # no healing

        self.current_health += amount
        self.variables.health_status = True

        if self.current_health > self.max_health:
            self.current_health = self.max_health
        return True  # healing == True

    def check_health(self, hunger=None):
        self.health_cooldown_timer += 1
        if self.current_health <= 0:
            self.death()

        if self.health_cooldown_timer >= 220:
            self.regenerate_health(hunger)
            self.health_cooldown_timer = 100
        
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def death(self):
        ### TODO: player moement disable.
        if self.variables.debug_mode == True:
            self.variables.ui_elements.append("""Debug mode, not closing the game.""")
        else:
            if self.death_start_time is None:
                self.death_start_time = time.perf_counter()

            elapsed_time = time.perf_counter() - self.death_start_time
            remaining_time = 5 - int(elapsed_time)

            if remaining_time >= 0:
                self.variables.ui_elements[-1] = f" You have died! Exiting game in {remaining_time} sec. "
            else:
                pygame.quit()

    def get_health(self):
        return self.current_health

    def __str__(self):
        if self.hunger is not None:
            if self.hunger <= 12:
                self.hunger = round(self.hunger, 3)
                if self.hunger <= 0:
                    return f"Health: {self.current_health}/{self.max_health}\n     -- Starvation Damage: {self.health_timer} ticks"

                else:
                    return f"Health: {self.current_health}/{self.max_health}\n     -- Regenerating Disabled, Too Hungry: {self.hunger}"

            else:
                return f"Health: {self.current_health}/{self.max_health}"

        else:
            return f"Health: {self.current_health}/{self.max_health}"


class StaminaComponent:
    stamina_bar_decay: int = 0

    def __init__(self, max_stamina, min_stamina, fading_text):
        self.fading_text = fading_text

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
    def __init__(self, base_hunger, max_hunger, min_hunger, fading_text):
        self.fading_text = fading_text

        self.hunger_timer = 100
        self.health_timer = 300
        self.base_hunger = base_hunger
        self.max_hunger = max_hunger
        self.min_hunger = min_hunger
        self.current_hunger = max(min_hunger, min(max_hunger, base_hunger))

    def update(self, health_cls_import):
        self.health = health_cls_import
        self.decrease_hunger()

    def get_hunger(self):
        return (self.current_hunger)

    def decrease_hunger(self):
        hunger_resist   = 2
        hunger_decrease = 0.1
        if self.variables.player_infected == True:
            hunger_resist   = 2
            hunger_decrease = 0.4
        if self.variables.hunger_resistance:
            self.variables.hunger_resistance -= hunger_resist
            if self.variables.hunger_resistance <= 0:
                self.variables.hunger_resistance = 0
                self.hunger_timer = 100
            return

        elif self.current_hunger <= 0:

            if self.health.health_timer <= 0:
                if self.health.current_health > 0:
                    self.fading_text.re_display_fading_text("Starving")

                self.health.damage(0.5)
                self.health.health_timer = 300
            self.health.health_timer -= 1
        else:
            if self.hunger_timer <= 0:
                self.current_hunger = max(self.min_hunger, self.current_hunger - hunger_decrease)
                self.hunger_timer = 100

            self.hunger_timer -= 1
            if self.health.health_timer < 300:
                self.health.health_timer = 300


    def __str__(self):
        rounded_hunger = round(self.current_hunger, 3)
        if rounded_hunger == self.min_hunger:
            return f"Hunger: {rounded_hunger}/{self.max_hunger}\n     -- Starving"
        else:
            if self.variables.hunger_resistance != 0:
                return f"Hunger: {rounded_hunger}/{self.max_hunger}\n     -- Hunger Resistance: {self.variables.hunger_resistance} ticks"
            else:
                return f"Hunger: {rounded_hunger}/{self.max_hunger}\n       -- Losing Hunger: {self.hunger_timer} ticks"


class ThirstComponent:
    def __init__(self, base_thirst, max_thirst, min_thirst, fading_text):
        self.fading_text = fading_text

        self.thirst_timer = 100
        self.base_thirst = base_thirst
        self.max_thirst = max_thirst
        self.min_thirst = min_thirst
        self.current_thirst = max(min_thirst, min(max_thirst, base_thirst))

    def update(self, health_cls_import):
        self.health = health_cls_import
        self.decrease_thirst()

    def get_thirst(self):
        return self.current_thirst

    def decrease_thirst(self):
        thirst_resist   = 1
        thirst_decrease = 0.07
        #if self.variables.player_infected == True:
        #    thirst_resist   = 2
        #    thirst_decrease = 0.4

        if self.variables.thirst_resistance:
            self.variables.thirst_resistance -= thirst_resist
            if self.variables.thirst_resistance <= 0:
                self.variables.thirst_resistance = 0
                self.thirst_timer = 100
            return

        elif self.current_thirst <= 0:
            if self.health.health_timer <= 0:
                if self.health.current_health > 0:
                    self.fading_text.re_display_fading_text("Dying from hydration.")

                self.health.damage(0.5)
                self.health.health_timer = 150
            self.health.health_timer -= 1

        else:
            if self.thirst_timer <= 0:
                self.current_thirst = max(self.min_thirst, self.current_thirst - thirst_decrease)
                self.thirst_timer = 100

            self.thirst_timer -= 1
            if self.health.health_timer < 150:
                self.health.health_timer = 150        
    
    def __str__(self):
        rounded_hunger = round(self.current_thirst, 3)
        return f'Thirst: {rounded_hunger}/{self.max_thirst}'


class Player:
    def __init__(self, max_health, min_health,
                 max_stamina, min_stamina,
                 base_speed, max_speed, min_speed,
                 base_hunger, max_hunger, min_hunger,
                 base_thirst, max_thirst, min_thirst,
                 fading_text):
        
        self.fading_text = fading_text  # redefine, et saaks kasutada argumendina componentites

        # playeri componentid on siin initialized, ei pea main game failis tegema!
        
        self.stamina = StaminaComponent(max_stamina=max_stamina,
                                        min_stamina=min_stamina, 
                                        fading_text=self.fading_text)
        
        self.speed = SpeedComponent(base_speed=base_speed,
                                    max_speed=max_speed,
                                    min_speed=min_speed)
        
        self.hunger = HungerComponent(base_hunger=base_hunger,
                                      max_hunger=max_hunger,
                                      min_hunger=min_hunger, 
                                      fading_text=self.fading_text)

        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health,
                                      fading_text=self.fading_text)
        
        self.thirst = ThirstComponent(base_thirst=base_thirst, 
                                      max_thirst=max_thirst,
                                      min_thirst=min_thirst, 
                                      fading_text=self.fading_text)

    def update(self):
        """ Update player components: health, hunger, thirst. """

        # Importanto!! ARGUMENDID on teised classid, mida imporditavad classid vajavad
        self.health.update(self.hunger)
        self.hunger.update(self.health)
        self.thirst.update(self.health)

    def apply_knockback(self, dx, dy):
        knockback_force = 35.0  # Knockback strength, 100.0 == 1 block size almost...
        self.variables.player_x += dx * knockback_force
        self.variables.player_y += dy * knockback_force

    def __str__(self):
        return f"Player stats:\n   {self.health}\n   {self.stamina}\n   {self.speed}\n   {self.hunger}\n   {self.thirst}\n  Inventory: {Inventory.inventory}\n"
