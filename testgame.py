import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('360 Degree Vision with Wall Occlusions')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define obstacles as rectangles
rectangles = [
    pygame.Rect(100, 100, 100, 100),
    pygame.Rect(300, 200, 150, 100),
    pygame.Rect(600, 400, 120, 150),
    pygame.Rect(100, 450, 200, 100),
]

# Light range
light_range = 300


def get_line_intersection(p0, p1, p2, p3):
    """Calculates the intersection point of two line segments if it exists."""
    s1_x, s1_y = p1[0] - p0[0], p1[1] - p0[1]
    s2_x, s2_y = p3[0] - p2[0], p3[1] - p2[1]

    denom = s1_x * s2_y - s2_x * s1_y
    if denom == 0: return None  # Parallel lines

    denom_is_positive = denom > 0
    s02_x, s02_y = p0[0] - p2[0], p0[1] - p2[1]
    s_numer = s1_x * s02_y - s1_y * s02_x
    t_numer = s2_x * s02_y - s2_y * s02_x

    if (s_numer < 0) == denom_is_positive or (t_numer < 0) == denom_is_positive or \
            (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive:
        return None  # No collision

    t = t_numer / denom
    intersection_point = (p0[0] + (t * s1_x), p0[1] + (t * s1_y))
    return intersection_point if 0 <= t <= 1 else None


def draw_visibility_polygon(screen, light_source, rectangles, light_range):
    # Calculate visibility polygon points
    polygon_points = calculate_visibility_polygon(light_source, rectangles, light_range)

    # Draw the visibility polygon
    if polygon_points:
        pygame.draw.polygon(screen, pygame.Color("gray"), polygon_points, 0)  # Fill the polygon


def calculate_visibility_polygon(light_source, rectangles, light_range):
    points = []
    # Cast rays at 360 degrees around the light source
    for angle in range(0, 360, 1):  # Adjust granularity as needed
        rad_angle = math.radians(angle)
        ray_end = (
            light_source[0] + math.cos(rad_angle) * light_range, light_source[1] + math.sin(rad_angle) * light_range)
        closest_intersection = get_closest_intersection(light_source, ray_end, rectangles)
        if closest_intersection:
            points.append(closest_intersection)
        else:
            points.append(ray_end)
    return points


def get_closest_intersection(light_source, ray_end, rectangles):
    closest_point = None
    min_dist = light_range
    for rect in rectangles:
        for edge in get_rectangle_edges(rect):
            intersection = get_line_intersection(light_source, ray_end, *edge)
            if intersection:
                dist = math.hypot(intersection[0] - light_source[0], intersection[1] - light_source[1])
                if dist < min_dist:
                    min_dist = dist
                    closest_point = intersection
    return closest_point


def get_rectangle_edges(rect):
    """Returns the edges of a rectangle as line segments."""
    return [
        (rect.topleft, rect.topright),
        (rect.topright, rect.bottomright),
        (rect.bottomright, rect.bottomleft),
        (rect.bottomleft, rect.topleft)
    ]


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        # Draw the comprehensive visibility including both direct and fill light effects
        draw_visibility_polygon(screen, (round(mouse_pos[0], 6), round(mouse_pos[1], 6)), rectangles, light_range)

        # Draw the rectangles (obstacles)
        for rect in rectangles:
            pygame.draw.rect(screen, WHITE, rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()

import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Custom Mouse Pointer")

# Load custom mouse pointer image
custom_pointer_img = pygame.image.load("custom_pointer.png")  # Replace "custom_pointer.png" with your image file

# Set default mouse pointer to invisible
pygame.mouse.set_visible(False)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Draw the custom mouse pointer image at the mouse position
    screen.blit(custom_pointer_img, (mouse_x, mouse_y))

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
