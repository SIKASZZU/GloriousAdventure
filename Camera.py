import pygame
import random

pygame.init()

# Set up display dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sectioned Camera Example")
clock = pygame.time.Clock()

# Define section dimensions and zoom factor
section_width, section_height = screen_width, screen_height

# Create a 2D array to represent sections and their colors
sections = [
    [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(3)]
    for _ in range(3)
]

# Initialize the camera position and player's initial spawn
camera_x, camera_y = 0, 0
current_section_x, current_section_y = 1, 1
player_x, player_y = section_width // 2, section_height // 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the player's position based on input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 5
    if keys[pygame.K_RIGHT]:
        player_x += 5
    if keys[pygame.K_UP]:
        player_y -= 5
    if keys[pygame.K_DOWN]:
        player_y += 5

    # Check if the player has moved to a different section
    new_section_x = player_x // section_width
    new_section_y = player_y // section_height

    if (new_section_x != current_section_x) or (new_section_y != current_section_y):
        current_section_x = new_section_x
        current_section_y = new_section_y
        camera_x = current_section_x * section_width
        camera_y = current_section_y * section_height

    # Clear the screen
    screen.fill((0, 0, 0))

    # Render game objects in the current section
    section_color = sections[current_section_y][current_section_x]
    section_rect = pygame.Rect(0, 0, section_width, section_height)
    pygame.draw.rect(screen, section_color, section_rect)

    # Render the player
    player_rect = pygame.Rect(player_x - camera_x - 10, player_y - camera_y - 10, 20, 20)
    pygame.draw.rect(screen, (255, 0, 0), player_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
