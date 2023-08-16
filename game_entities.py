from components import HealthComponent
from components import StaminaComponent
from components import SpeedComponent

import time


class Player:
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
