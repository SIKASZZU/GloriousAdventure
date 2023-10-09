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
