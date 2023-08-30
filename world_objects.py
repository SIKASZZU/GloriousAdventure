from components import HealthComponent


class Tree:

    """
    Initialize a Tree object with attributes related to health and regeneration.

    Args:
        max_health (float): The maximum health value for the tree.
        min_health (float): The minimum health value for the tree.
    """

    def __init__(self, max_health, min_health, value, image):
        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health)
        self.value = value
        self.image = image


class Stump:

    """
    Initialize a Stump object with attributes related to health and regeneration.

    Args:
        max_health (float): The maximum health value for the stump.
        min_health (float): The minimum health value for the stump.
    """

    def __init__(self, max_health, min_health, value):
        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health)
        self.value = value


class Stone:

    """
    Initialize a Stone object with attributes related to health and regeneration.

    Args:
        max_health (float): The maximum health value for the stone.
        min_health (float): The minimum health value for the stone.
    """

    def __init__(self, max_health, min_health, value):
        self.health = HealthComponent(max_health=max_health,
                                      min_health=min_health)
        self.value = value

