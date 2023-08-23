import time
import math


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

    def __init__(self, max_health, min_health, health_regeneration_rate):
        self.max_health = max_health
        self.min_health = min_health
        self.current_health = max(min_health, min(max_health, max_health))
        self.health_regeneration_rate = health_regeneration_rate
        self.health_last_update_time = time.time()

    def health_regenerate(self):
        if self.health_last_update_time is None:
            return

        health_regenerate_elapsed_time = time.time() - self.health_last_update_time
        stamina_regained = health_regenerate_elapsed_time * self.health_regeneration_rate
        rounded_stamina_regained = math.floor(stamina_regained)
        self.current_health = min(self.current_health + rounded_stamina_regained, self.max_health)
        self.health_last_update_time = time.time()

    def heal(self, amount):
        self.current_health = min(self.current_health + amount, self.max_health)

    def damage(self, amount):
        self.current_health = max(self.current_health - amount, self.min_health)

    def get_health(self):
        return self.current_health


class StaminaComponent:

    """
    Represents a stamina component that manages the stamina of an object.

    Correct usage:
      StaminaComponent(max_stamina, min_stamina, stamina_regeneration_rate, degeneration_rate)
        OBJECT.command(*args, **kwargs)

    'use_stamina(self, amount):'
      Use a specified amount of stamina. Decreases the current stamina and updates the last update time
      for regeneration calculations.

    'degenerate(self):'
      Simulate gradual loss of stamina over time based on the degeneration rate.
      Updates the last update time for regeneration calculations.

    'stamina_regenerate(self):'
      Calculate and apply stamina regeneration based on elapsed time and the regeneration rate.
      Ensures that the regenerated stamina is rounded down to the nearest whole number using math.floor.

    'get_stamina(self):'
      Retrieve the current stamina value while applying regeneration if needed.

    Args:
      max_stamina (float): The maximum stamina value the component can hold.
      min_stamina (float): The minimum stamina value the component can have.
      stamina_regeneration_rate (float): The rate at which stamina regenerates, in stamina points per second.
      stamina_degeneration_rate (float): The rate at which stamina degenerates, in stamina points per second.
    """

    def __init__(self, max_stamina, min_stamina, stamina_regeneration_rate, stamina_degeneration_rate):
        self.max_stamina = max_stamina
        self.min_stamina = min_stamina
        self.current_stamina = max(min_stamina, min(max_stamina, max_stamina))
        self.stamina_regeneration_rate = stamina_regeneration_rate
        self.stamina_degeneration_rate = stamina_degeneration_rate
        self.stamina_last_update_time = time.time()

    def use_stamina(self, amount):
        self.current_stamina = round(max(self.current_stamina - amount, self.min_stamina), 3)
        self.stamina_last_update_time = time.time()

    def stamina_regenerate(self, amount):
        if self.current_stamina >= self.max_stamina:
            self.max_stamina = 20
        else:
            self.current_stamina = round(self.current_stamina + amount, 3)

    def get_stamina(self):
        return self.current_stamina


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
