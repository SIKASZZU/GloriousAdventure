"""Seda faili peab manuaalselt pushima. Gitignores ignorerib seda, et meil speediga conflict ei tekiks"""
from components import HealthComponent
from components import HungerComponent
from components import SpeedComponent
from components import HitBoxComponent
from stamina import StaminaComponent
from components import AttackComponent

# hunger / hitbox / attack - pole tehtud

class Player:

    """
    Initialize a Player object with various attributes related to health, stamina, and speed.

    Args:
        max_health (float): The maximum health value for the player.
        min_health (float): The minimum health value for the player.

        max_stamina (float): The maximum stamina value for the player.
        min_stamina (float): The minimum stamina value for the player.

        base_speed (float): The base speed of the player.
        max_speed (float): The maximum speed the player can achieve.
        min_speed (float): The minimum speed the player can have.
    """

    def __init__(self, max_health, min_health,
                max_stamina, min_stamina,
                base_speed, max_speed, min_speed):

        self.health = HealthComponent(max_health=max_health,
                                    min_health=min_health)

        self.stamina = StaminaComponent(max_stamina=max_stamina, 
                                    min_stamina=min_stamina)

        self.speed= SpeedComponent(base_speed=base_speed, 
                                max_speed=max_speed, 
                                min_speed=min_speed)

player_stats = Player(max_health=20, min_health=0, max_stamina=20, min_stamina=0, base_speed=4, max_speed=10, min_speed=1)