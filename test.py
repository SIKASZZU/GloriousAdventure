# # defining a decorator
# def hello_decorator(func):
#     # inner1 is a Wrapper function in
#     # which the argument is called
#
#     # inner function can access the outer local
#     # functions like in this case "func"
#     def inner1():
#         print("Hello, this is before function execution.")
#
#         # calling the actual function now
#         # inside the wrapper function.
#         func()
#
#         print("This is after function execution.")
#
#     return inner1
#
#
# # defining a function, to be called inside wrapper
# @hello_decorator
# def function_to_be_used():
#     print("This is inside the function.")
#
# function_to_be_used()
#
# import pygame
#
# # Initialize Pygame
# pygame.init()
#
# # Set up the screen
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption('Fixed Update Test')
#
# # Game variables
# x = 50
# y = 50
# speed = 5
#
# # FPS settings
# UPDATE_RATE = 60
# update_clock = pygame.time.Clock()
# render_clock = pygame.time.Clock()
#
# # Font initialization
# font = pygame.font.Font(None, 36)  # Change 'None' to a font file path for a specific font
#
# # Game loop
# running = True
# previous_time = pygame.time.get_ticks()
# delta_time = 0
# while running:
#     # Calculate delta time
#     current_time = pygame.time.get_ticks()
#     delta_time += current_time - previous_time
#     previous_time = current_time
#
#     # Update game logic at fixed rate
#     while delta_time >= 1000 / UPDATE_RATE:
#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#         # Game logic update
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_d]:
#             x += speed
#         if keys[pygame.K_a]:
#             x -= speed
#         if keys[pygame.K_s]:
#             y += speed
#         if keys[pygame.K_w]:
#             y -= speed
#
#         # Ensure the object stays within the screen boundaries
#         x = max(0, min(x, 750))
#         y = max(0, min(y, 550))
#
#         delta_time -= 1000 / UPDATE_RATE
#
#     # Render the game as fast as possible
#     screen.fill((0, 0, 0))  # Clear screen
#     pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, 50, 50))  # Draw a red rectangle
#
#     # Display FPS count on the screen
#     fps_text = font.render(f"FPS: {int(render_clock.get_fps())}", True, (255, 255, 255))
#     screen.blit(fps_text, (10, 10))
#
#     pygame.display.flip()  # Update the display
#     render_clock.tick()  # Measure the actual FPS for rendering
#
# # Quit Pygame properly
# pygame.quit()
#
#
# import multiprocessing
# import time
#
# def task(n):
#     # Your task logic here
#     print(f"Task {n} started")
#     # Simulate some work
#     for _ in range(1000000):
#         pass
#     print(f"Task {n} completed")
#
# def main():
#     # Number of tasks to execute
#     num_tasks = 10000
#
#     # Create a Pool with, for example, 4 worker processes
#     with multiprocessing.Pool(processes=16) as pool:
#         # Map the task function to each item in the range to execute them concurrently
#         pool.map(task, range(num_tasks))
#
# if __name__ == "__main__":
#     start_time = time.time()
#     main()
#     print(f"Execution time: {time.time() - start_time} seconds")

# import pygame
# import sys
# import random
#
# pygame.init()
#
# # Set up the screen
# screen = pygame.display.set_mode((400, 300))
# clock = pygame.time.Clock()
#
# # Load the sprite sheet image
# sprite_sheet = pygame.image.load("images/Sprites/Worm.png")
#
# # Define the dimensions of each frame
# frame_width = 64
# frame_height = 64
#
# # Scale the sprite sheet
# sprite_sheet = pygame.transform.scale(sprite_sheet, (frame_width * 8, frame_height * 8))
#
# # Calculate the maximum number of frames that can fit within the image width
# max_frames = min(sprite_sheet.get_width() // frame_width, 8)
#
# # Define frames for left and right movements
# right_frames = [sprite_sheet.subsurface(((max_frames - 1 - i) * frame_width, frame_height, frame_width, frame_height))
#                for i in range(max_frames)]
# left_frames = [sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
#                 for i in range(max_frames)]
#
# # Create frames for up and down movements
# up_frames = [sprite_sheet.subsurface((i * frame_width, frame_height * 2, frame_width, frame_height))
#              for i in range(max_frames)]
# down_frames = [sprite_sheet.subsurface((i * frame_width, frame_height * 3, frame_width, frame_height))
#                for i in range(max_frames)]
#
# idle_left_frames = [sprite_sheet.subsurface((i * frame_width, frame_height * 4, frame_width, frame_height))
#                for i in range(max_frames)]
# idle_right_frames = [sprite_sheet.subsurface((i * frame_width, frame_height * 5, frame_width, frame_height))
#                for i in range(max_frames)]
# idle_up_frames = [sprite_sheet.subsurface((i * frame_width, frame_height * 6, frame_width, frame_height))
#                for i in range(max_frames)]
# idle_down_frames = [sprite_sheet.subsurface((i * frame_width, frame_height * 7, frame_width, frame_height))
#                for i in range(max_frames)]
# # Combine all frames into the dictionary
# frames = {
#     "right": right_frames,
#     "left": left_frames,
#     "up": up_frames,
#     "down": down_frames,
#     "idle_left": idle_left_frames,
#     "idle_right": idle_right_frames,
#     "idle_up": idle_up_frames,
#     "idle_down": idle_down_frames,
# }
#
# # Starting position of the sprite
# sprite_x = 100
# sprite_y = 100
#
# # Initial direction and movement
# last_direction = "right"
# current_frames = frames["right"]
# frame_index = 0
#
# # Time variables for idle animations
# time_since_last_movement = pygame.time.get_ticks()
# idle_duration = 0  # 3 seconds (in milliseconds)
#
# while True:
#     screen.fill((0, 0, 0))
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#     keys = pygame.key.get_pressed()
#
#     # Move the sprite based on arrow key inputs
#     move_increment = 2  # Movement speed
#     if keys[pygame.K_UP]:
#         current_frames = frames["up"]
#         sprite_y -= move_increment
#         last_direction = "up"
#         time_since_last_movement = pygame.time.get_ticks()
#     elif keys[pygame.K_DOWN]:
#         current_frames = frames["down"]
#         sprite_y += move_increment
#         last_direction = "down"
#         time_since_last_movement = pygame.time.get_ticks()
#     elif keys[pygame.K_LEFT]:
#         current_frames = frames["left"]
#         sprite_x -= move_increment
#         last_direction = "left"
#         time_since_last_movement = pygame.time.get_ticks()
#     elif keys[pygame.K_RIGHT]:
#         current_frames = frames["right"]
#         sprite_x += move_increment
#         last_direction = "right"
#         time_since_last_movement = pygame.time.get_ticks()
#
#     # Check if the player has been idle for a certain duration
#     current_time = pygame.time.get_ticks()
#     if current_time - time_since_last_movement > idle_duration:
#         # Choose idle animation based on the last movement
#         current_frames = frames[f"idle_{last_direction}"]
#
#     # Update the frame index for animation
#     frame_index = (frame_index + 1) % len(current_frames)
#
#     # Display the current frame and position the sprite
#     if current_frames:  # Check if current_frames is not empty
#         screen.blit(current_frames[frame_index], (sprite_x, sprite_y))
#     else:
#         print("No frames found for the current direction.")
#
#     pygame.display.flip()
#     clock.tick(10)  # Adjust the speed of the animation (frames per second)
#

import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from skimage.transform import resize

def generate_perlin_noise_2d(shape, res):
    """
    Generate a 2D numpy array of perlin noise.
    """
    def f(t):
        return 6*t**5 - 15*t**4 + 10*t**3

    grid = np.mgrid[0:res[0],0:res[1]].transpose(1, 2, 0)
    grid = grid / res

    gradients = np.random.rand(res[0] + 1, res[1] + 1, 2)
    gradients /= np.linalg.norm(gradients, axis=2, keepdims=True)

    g00 = gradients[:-1,:-1]
    g10 = gradients[1:,:-1]
    g01 = gradients[:-1,1:]
    g11 = gradients[1:,1:]

    t = grid - grid.astype(int)
    fade_t = f(t)

    n00 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1])) * g00, axis=2)
    n10 = np.sum(np.dstack((grid[:,:,0] - 1, grid[:,:,1])) * g10, axis=2)
    n01 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1] - 1)) * g01, axis=2)
    n11 = np.sum(np.dstack((grid[:,:,0] - 1, grid[:,:,1] - 1)) * g11, axis=2)

    n0 = n00 * (1 - fade_t[:,:,0]) + n10 * fade_t[:,:,0]
    n1 = n01 * (1 - fade_t[:,:,0]) + n11 * fade_t[:,:,0]

    noise = np.sqrt(2) * (n0 * (1 - fade_t[:,:,1]) + n1 * fade_t[:,:,1])
    return noise

def create_maze_with_perlin_noise(size, resolution, start_side):
    noise = generate_perlin_noise_2d((size, size), resolution)
    noise_resized = resize(noise, (size, size), mode='reflect')
    maze = np.where(noise_resized > np.percentile(noise_resized, 75), '*', ' ')  # threshold adjusted to create more walls

    # Ensure outer walls
    maze[0, :] = maze[-1, :] = '*'
    maze[:, 0] = maze[:, -1] = '*'

    # Set the start point
    if start_side == 'top':
        start = (0, random.randint(1, size-2))
    elif start_side == 'bottom':
        start = (size-1, random.randint(1, size-2))
    elif start_side == 'left':
        start = (random.randint(1, size-2), 0)
    elif start_side == 'right':
        start = (random.randint(1, size-2), size-1)
    maze[start] = 'S'

    # Set the end points on the remaining three sides
    sides = ['top', 'bottom', 'left', 'right']
    sides.remove(start_side)
    for side in sides:
        if side == 'top':
            end = (0, random.randint(1, size-2))
        elif side == 'bottom':
            end = (size-1, random.randint(1, size-2))
        elif side == 'left':
            end = (random.randint(1, size-2), 0)
        elif side == 'right':
            end = (random.randint(1, size-2), size-1)
        maze[end] = 'E'

    return maze

# Create a 40x40 maze with the start point on the left side
maze_size = 40
resolution = (40, 40)  # Adjusted resolution of Perlin noise for more distributed walls
start_side = 'left'

maze = create_maze_with_perlin_noise(maze_size, resolution, start_side)

# Display the maze as text
for row in maze:
    print(' '.join(row))
