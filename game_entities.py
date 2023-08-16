from components import HealthComponent
from components import StaminaComponent
from components import SpeedComponent

import time


class Player:
    
    """
    Initialize a Player object with various attributes related to health, stamina, and speed.

    Args:
        max_health (float): The maximum health value for the player.
        min_health (float): The minimum health value for the player.
        health_regeneration_rate (float): The rate at which health regenerates for the player.

        max_stamina (float): The maximum stamina value for the player.
        min_stamina (float): The minimum stamina value for the player.
        stamina_regeneration_rate (float): The rate at which stamina regenerates for the player.
        stamina_degeneration_rate (float): The rate at which stamina decreases over time.

        base_speed (float): The base speed of the player.
        max_speed (float): The maximum speed the player can achieve.
        min_speed (float): The minimum speed the player can have.
    """
        
    def __init__(self, max_health, min_health, health_regeneration_rate,
                 max_stamina, min_stamina, stamina_regeneration_rate, stamina_degeneration_rate,
                 base_speed, max_speed, min_speed):

        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health,
                                      health_regeneration_rate=health_regeneration_rate)

        self.stamina = StaminaComponent(max_stamina=max_stamina,
                                        min_stamina=min_stamina,
                                        stamina_regeneration_rate=stamina_regeneration_rate,
                                        stamina_degeneration_rate=stamina_degeneration_rate)

        self.speed = SpeedComponent(base_speed=base_speed,
                                    max_speed=max_speed,
                                    min_speed=min_speed)
