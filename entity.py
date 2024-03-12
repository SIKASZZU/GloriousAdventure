import random
import pygame
import math

from images import ImageLoader

animal_sprites = pygame.sprite.RenderUpdates()
mob_sprites = pygame.sprite.RenderUpdates()


def add_animals():
    sheep_image = ImageLoader.load_sprite_image("Sheep")
    cow_image = ImageLoader.load_sprite_image("Cow")

    # Resizing images
    sheep_image = pygame.transform.scale(sheep_image, (int(sheep_image.get_width() * 2), int(sheep_image.get_height() * 2)))
    cow_image = pygame.transform.scale(cow_image, (int(cow_image.get_width() * 4), int(cow_image.get_height() * 4)))

    sheep = Animal(10, 1, sheep_image, (random.randint(300, 600), random.randint(300, 500)), "Sheep")
    cow = Animal(15, 1, cow_image, (random.randint(300, 600), random.randint(300, 500)), "Cow")

    animal_sprites.add(sheep, cow)


class Entity(pygame.sprite.Sprite):

    def __init__(self, health, speed, image, position):
        super().__init__()
        self.health = health  # Health of the entity
        self.speed = speed  # Movement speed of the entity
        self.image = image  # Image representing the entity
        self.rect = self.image.get_rect()  # Rectangle defining the entity's size and position
        self.rect.center = position  # Set the initial position of the entity

    def update(self, *args, **kwargs):
        # Update the sprite's position and other properties here
        pass


class Mob(Entity):
    def __init__(self, health, speed, image, position):
        super().__init__(health, speed, image, position)

    def update(self, *args, **kwargs):
        # Add enemy-specific update logic here
        # Ai logic, et playerit attakima hakkaks
        pass


class Animal(Entity):
    """
    Represents an animal entity in the game, inheriting from the Entity class.
    Handles the behavior, movement, and health of the animal.
    """

    def __init__(self, health: int, speed: float, image: pygame.Surface, position: tuple, name: str) -> None:
        """
        Initialize the Animal instance.

        :param health: The health of the animal.
        :param speed: The movement speed of the animal.
        :param image: The visual representation (sprite) of the animal.
        :param position: The initial position of the animal as (x, y).
        :param name: The name of the animal (e.g., 'Sheep', 'Cow').
        """
        super().__init__(health, speed, image, position)
        self.name = name
        self.health = health
        self.original_speed = speed
        self.speed = speed

        self.direction = pygame.Vector2(0, 0)
        self.was_hit = False
        self.moving = random.choice([True, False])
        self.last_update = 0
        self.move_duration = 0
        self.stand_duration = 0
        self.move_counter = 0

    def __str__(self) -> str:
        """
        Returns a string representation of the Animal instance.

        :return: String representing the animal's current position and health.
        """
        return f"Animal: Position=({self.rect.x}, {self.rect.y}), Health={self.health}"

    def set_new_behavior(self) -> None:
        """
        Determines and sets the new behavior for the animal, either moving or standing still.
        """
        if self.move_counter > 0:
            self.move()
            self.move_counter -= 1
            if self.move_counter == 0:
                self.speed = self.original_speed

        elif random.choice([True, True, True, False]):
            self.move()

        else:
            self.moving = False
            self.was_hit = False
            self.stand_duration = random.randint(1, 7) * 1000
            self.last_update = pygame.time.get_ticks()

    def move(self) -> None:
        """
        Initiates movement for the animal.
        """
        self.moving = True
        self.move_duration = random.uniform(0.7, 1.2) * 1000 if self.was_hit else random.uniform(0.2, 0.7) * 1000
        angle = random.uniform(0, 2 * math.pi)
        self.direction = pygame.Vector2(math.cos(angle), math.sin(angle)).normalize() * self.speed
        self.last_update = pygame.time.get_ticks()

    def update(self, *args, **kwargs) -> None:
        """
        Updates the animal's state. This method is called every frame.

        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        current_time = pygame.time.get_ticks()

        if self.moving:
            self.rect.x += self.direction.x * self.speed
            self.rect.y += self.direction.y * self.speed
            if current_time - self.last_update > self.move_duration:
                self.set_new_behavior()
        else:
            if current_time - self.last_update > self.stand_duration:
                self.set_new_behavior()

    def hit(self, damage_taken: int) -> None:
        """
        Applies damage to the animal and updates its state accordingly.

        :param damage_taken: The amount of damage to apply to the animal.
        """
        self.health -= damage_taken
        if self.health <= 1:
            self.die()
        else:
            self.was_hit = True
            self.speed *= 2  # Increase speed by 2 times when hit
            self.move_counter = 3
            self.move()
            print(f"\nOuch! The {self.name} took {damage_taken} damage! \nCurrent health: {self.health}.")

    def die(self) -> None:
        """
        Handles the death of the animal.
        """
        print(f"\nThe {self.name} has died at {self.rect.center}.")
        animal_sprites.remove(self)
