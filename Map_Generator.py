import pygame
import random
import math

# Define terrain types
LAND = 0
WATER = 1
DEEP_WATER = 2

# Pygame setup
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def generate_noise(width, height, scale):
    noise_grid = []
    for y in range(height):
        row = []
        for x in range(width):
            value = random.uniform(-1, 1)
            row.append(value)
        noise_grid.append(row)
    return noise_grid

def interpolate(a, b, t):
    return a * (1 - t) + b * t

def smooth_noise(noise_grid, x, y):
    fraction_x = x - int(x)
    fraction_y = y - int(y)

    x1 = int(x) % len(noise_grid[0])
    y1 = int(y) % len(noise_grid)
    x2 = (x1 + 1) % len(noise_grid[0])
    y2 = (y1 + 1) % len(noise_grid)

    value = 0.0
    value += interpolate(noise_grid[y1][x1], noise_grid[y1][x2], fraction_x) * (1 - fraction_y)
    value += interpolate(noise_grid[y2][x1], noise_grid[y2][x2], fraction_x) * fraction_y
    return value

def generate_terrain(width, height, scale, octaves, persistence, lacunarity):
    noise_grid = generate_noise(width, height, scale)
    terrain = []
    for y in range(height):
        row = []
        for x in range(width):
            value = 0.0
            frequency = 1
            amplitude = 1
            for _ in range(octaves):
                value += smooth_noise(noise_grid, x * frequency / scale, y * frequency / scale) * amplitude
                frequency *= lacunarity
                amplitude *= persistence
            row.append(value)
        terrain.append(row)
    return terrain

def generate_terrain_types(terrain, water_threshold, deep_water_threshold):
    terrain_types = []
    for y in range(len(terrain)):
        row = []
        for x in range(len(terrain[0])):
            value = terrain[y][x]
            if value < deep_water_threshold:
                row.append(DEEP_WATER)
            elif value < water_threshold:
                row.append(WATER)
            else:
                row.append(LAND)
        terrain_types.append(row)
    return terrain_types

def render_terrain(terrain_types):
    for y, row in enumerate(terrain_types):
        for x, terrain_type in enumerate(row):
            if terrain_type == DEEP_WATER:
                color = (0, 0, 192)  # Light blue for deeper water
            elif terrain_type == WATER:
                color = (0, 0, 255)  # Blue for water
            elif terrain_type == LAND:
                color = (0, 100, 0)  # Dark green for land
            pygame.draw.rect(screen, color, (x, y, 1, 1))

# Terrain generation parameters
scale = 50
octaves = 6
persistence = 0.5
lacunarity = 2.0

terrain = generate_terrain(width, height, scale, octaves, persistence, lacunarity)

water_threshold = 0.3  # Adjust these thresholds as needed
deep_water_threshold = 0.2

terrain_types = generate_terrain_types(terrain, water_threshold, deep_water_threshold)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    render_terrain(terrain_types)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
