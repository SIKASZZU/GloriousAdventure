from components import HealthComponent


class Tree:
    def __init__(self, max_health, min_health, health_regeneration_rate):
        """
        Initialize a Tree object with attributes related to health and regeneration.

        Args:
            max_health (float): The maximum health value for the tree.
            min_health (float): The minimum health value for the tree.
            health_regeneration_rate (float): The rate at which health regenerates for the tree.
        """
        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health,
                                      health_regeneration_rate=health_regeneration_rate)


class Stump:
    def __init__(self, max_health, min_health, health_regeneration_rate):
        """
        Initialize a Stump object with attributes related to health and regeneration.

        Args:
            max_health (float): The maximum health value for the stump.
            min_health (float): The minimum health value for the stump.
            health_regeneration_rate (float): The rate at which health regenerates for the stump.
        """
        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health,
                                      health_regeneration_rate=health_regeneration_rate)


class Stone:
    def __init__(self, max_health, min_health, health_regeneration_rate):
        """
        Initialize a Stone object with attributes related to health and regeneration.

        Args:
            max_health (float): The maximum health value for the stone.
            min_health (float): The minimum health value for the stone.
            health_regeneration_rate (float): The rate at which health regenerates for the stone.
        """
        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health,
                                      health_regeneration_rate=health_regeneration_rate)
