# defining a decorator
def hello_decorator(func):
    # inner1 is a Wrapper function in
    # which the argument is called

    # inner function can access the outer local
    # functions like in this case "func"
    def inner1():
        print("Hello, this is before function execution.")

        # calling the actual function now
        # inside the wrapper function.
        func()

        print("This is after function execution.")

    return inner1


# defining a function, to be called inside wrapper
@hello_decorator
def function_to_be_used():
    print("This is inside the function.")

function_to_be_used()

import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Fixed Update Test')

# Game variables
x = 50
y = 50
speed = 5

# FPS settings
UPDATE_RATE = 60
update_clock = pygame.time.Clock()
render_clock = pygame.time.Clock()

# Font initialization
font = pygame.font.Font(None, 36)  # Change 'None' to a font file path for a specific font

# Game loop
running = True
previous_time = pygame.time.get_ticks()
delta_time = 0
while running:
    # Calculate delta time
    current_time = pygame.time.get_ticks()
    delta_time += current_time - previous_time
    previous_time = current_time

    # Update game logic at fixed rate
    while delta_time >= 1000 / UPDATE_RATE:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic update
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            x += speed
        if keys[pygame.K_a]:
            x -= speed
        if keys[pygame.K_s]:
            y += speed
        if keys[pygame.K_w]:
            y -= speed

        # Ensure the object stays within the screen boundaries
        x = max(0, min(x, 750))
        y = max(0, min(y, 550))

        delta_time -= 1000 / UPDATE_RATE

    # Render the game as fast as possible
    screen.fill((0, 0, 0))  # Clear screen
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, 50, 50))  # Draw a red rectangle

    # Display FPS count on the screen
    fps_text = font.render(f"FPS: {int(render_clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()  # Update the display
    render_clock.tick()  # Measure the actual FPS for rendering

# Quit Pygame properly
pygame.quit()


import pygame
import os

# Initialize Pygame
pygame.init()

# Set window size
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Image Blitting and Resizing")

# Load image
image_path = "images/Main_Menu.jpg"  # Replace with your image path
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image not found at {image_path}")
original_image = pygame.image.load(image_path).convert()  # Load and convert for better performance

# Resize image to fit window
image = pygame.transform.scale(original_image, (window_width, window_height))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Blit the image onto the screen
    window.blit(image, (0, 0))

    # Update the display
    pygame.display.update()

pygame.quit()
