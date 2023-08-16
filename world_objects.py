from components import HealthComponent


class Tree:
    def __init__(self, max_health, min_health, health_regeneration_rate):
        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health,
                                      health_regeneration_rate=health_regeneration_rate)
