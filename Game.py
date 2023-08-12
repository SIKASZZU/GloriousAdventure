import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 750

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Character properties
character_size = 30  # Reduced character size
character_speed = 3

# Terrain data
terrain_data = [
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 0, 2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0, 4, 4, 4, 4],
    [4, 4, 4, 4, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
    [4, 4, 4, 4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 4, 4, 4],
    [4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4],
    [4, 4, 4, 4, 0, 0, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4, 4],
    [4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 1, 0, 0, 4, 4, 4],
    [4, 4, 4, 4, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4],
    [4, 4, 4, 4, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
]


# Find a valid spawn location that is not water
def find_valid_spawn():
    while True:
        x = random.randint(0, len(terrain_data[0]) - 1)
        y = random.randint(0, len(terrain_data) - 1)
        if terrain_data[y][x] != 4:
            return x * 50, y * 50

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Controllable Character")

# Get a valid spawn location for the character
character_x, character_y = find_valid_spawn()

# Clear the screen once
screen.fill(BLUE)  # Use the blue color as the background
pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Calculate the character's potential new position
    new_character_x = character_x
    new_character_y = character_y
    if keys[pygame.K_a]:  # Left
        new_character_x -= character_speed
    if keys[pygame.K_d]:  # Right
        new_character_x += character_speed
    if keys[pygame.K_w]:  # Up
        new_character_y -= character_speed
    if keys[pygame.K_s]:  # Down
        new_character_y += character_speed

    # Check if the potential new position is valid (not water) at each corner
    corners = [
        (new_character_x, new_character_y),
        (new_character_x + character_size, new_character_y),
        (new_character_x, new_character_y + character_size),
        (new_character_x + character_size, new_character_y + character_size)
    ]
    valid_move = True
    for corner_x, corner_y in corners:
        corner_grid_x = corner_x // 50
        corner_grid_y = corner_y // 50
        if (
            corner_grid_x < 0 or corner_grid_x >= len(terrain_data[0]) or
            corner_grid_y < 0 or corner_grid_y >= len(terrain_data)
        ):
            valid_move = False
            break
        if terrain_data[int(corner_grid_y)][int(corner_grid_x)] == 4:
            if (
                keys[pygame.K_a] and corner_grid_x != int(character_x // 50) and corner_grid_y == int(character_y // 50)
            ) or (
                keys[pygame.K_w] and corner_grid_y != int(character_y // 50) and corner_grid_x == int(character_x // 50)
            ):
                valid_move = True
            else:
                valid_move = False
            break

    if valid_move:
        character_x = new_character_x
        character_y = new_character_y

    # Calculate camera position to center on the character
    camera_x = character_x - SCREEN_WIDTH // 2
    camera_y = character_y - SCREEN_HEIGHT // 2

    # Copy the previous frame to the screen
    screen.fill(BLUE)  # Clear the screen with the blue color

    # Draw terrain and character on the updated frame
    for y, row in enumerate(terrain_data):
        for x, terrain_type in enumerate(row):
            terrain_color = GREEN if terrain_type == 0 else BROWN if terrain_type == 1 else GRAY if terrain_type == 2 else BLUE
            pygame.draw.rect(screen, terrain_color, (x * 50 - camera_x, y * 50 - camera_y, 50, 50))

    pygame.draw.rect(screen, YELLOW, (character_x - camera_x, character_y - camera_y, character_size, character_size))

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
