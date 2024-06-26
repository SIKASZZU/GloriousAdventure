import pygame
import math
import sys

# Constants
eps = 0.00001
angle_offset = 0.0001
screen_width = 800
screen_height = 600

player_color = (0, 255, 0, 255)  # Semi-transparent gray
polygon_color = (255, 255, 255, 100)  # Semi-transparent gray

segments_width = 3
ray_width = 1
player_radius = 5


# Helper classes
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


def get_offsetted_ray_point(ray, angle):
    dx, dy = ray[1].x - ray[0].x, ray[1].y - ray[0].y
    return Point(
        dx * math.cos(angle) - dy * math.sin(angle) + ray[0].x,
        dy * math.cos(angle) + dx * math.sin(angle) + ray[0].y
    )


def sort_intersection_points_by_angle(anchor, points):
    return sorted(points, key=lambda p: math.atan2(p.y - anchor.y, p.x - anchor.x))


def get_intersection_point(ray, segment, smallest_r=None):
    A, B = segment.p1, segment.p2
    C, D = ray
    denominator = (D.x - C.x) * (B.y - A.y) - (B.x - A.x) * (D.y - C.y)

    if denominator == 0:
        return None

    r = ((B.x - A.x) * (C.y - A.y) - (C.x - A.x) * (B.y - A.y)) / denominator
    if r < -eps or (smallest_r is not None and r > smallest_r):
        return None

    s = ((A.x - C.x) * (D.y - C.y) - (D.x - C.x) * (A.y - C.y)) / denominator
    if s < -eps or s > 1 + eps:
        return None

    return Point(s * (B.x - A.x) + A.x, s * (B.y - A.y) + A.y)


def get_closest_intersection_point(ray, segments):
    closest_point = None
    smallest_r = None

    for segment in segments:
        intersection_point = get_intersection_point(ray, segment, smallest_r)
        if intersection_point:
            if ray[1].x != ray[0].x:
                smallest_r = (intersection_point.x - ray[0].x) / (ray[1].x - ray[0].x)
            elif ray[1].y != ray[0].y:
                smallest_r = (intersection_point.y - ray[0].y) / (ray[1].y - ray[0].y)
            closest_point = intersection_point

    return closest_point


def draw_polygon(surface, points, color):
    if points:
        pygame.draw.polygon(surface, color, [(p.x, p.y) for p in points])


def draw_ray(screen, ray, color, width):
    pygame.draw.line(screen, color, (ray[0].x, ray[0].y), (ray[1].x, ray[1].y), width)


def draw_player(screen, player):
    pygame.draw.circle(screen, player_color, (int(player.x), int(player.y)), player_radius)


def calculate_vision_polygon(player, screen_width, screen_height, segments):
    vision_polygon = []

    for angle in range(-45, 46, 5):  # Adjust the angle range as needed
        rad_angle = math.radians(angle)
        ray_end_x = player.x + screen_width * math.cos(rad_angle)
        ray_end_y = player.y - screen_height * math.sin(rad_angle)  # Negative sin because y-axis is flipped
        ray_end_point = Point(ray_end_x, ray_end_y)

        closest_point = get_closest_intersection_point([player, ray_end_point], segments)
        if closest_point:
            vision_polygon.append(closest_point)

    return vision_polygon


# Set up
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('pygame')

# Obstacles
segments = [
    Segment(Point(0, 0), Point(800, 0)),
    Segment(Point(800, 0), Point(800, 300)),
    Segment(Point(800, 300), Point(0, 300)),
    Segment(Point(0, 300), Point(0, 0)),
    Segment(Point(300, 50), Point(350, 50)),
    Segment(Point(300, 50), Point(300, 100)),
    Segment(Point(500, 50), Point(450, 50)),
    Segment(Point(500, 50), Point(500, 100)),
    Segment(Point(300, 250), Point(350, 250)),
    Segment(Point(300, 250), Point(300, 200)),
    Segment(Point(500, 250), Point(450, 250)),
    Segment(Point(500, 250), Point(500, 200)),
    Segment(Point(200, 50), Point(200, 250)),
    Segment(Point(600, 50), Point(600, 250))
]

vertices = [segment.p1 for segment in segments] + [segment.p2 for segment in segments]

player = Point(screen_width / 2, screen_height / 2)
clock = pygame.time.Clock()

# Create a transparent surface for the polygon
poly_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= 5
    if keys[pygame.K_d]:
        player.x += 5
    if keys[pygame.K_w]:
        player.y -= 5
    if keys[pygame.K_s]:
        player.y += 5

    screen.fill("gray")

    intersection_points = []
    extra_intersection_points = []
    for vertex in vertices:
        ray = [player, vertex]
        extra_ray1 = [player, get_offsetted_ray_point(ray, -angle_offset)]
        extra_ray2 = [player, get_offsetted_ray_point(ray, angle_offset)]

        closest_point = get_closest_intersection_point(ray, segments)
        extra_closest_point1 = get_closest_intersection_point(extra_ray1, segments)
        extra_closest_point2 = get_closest_intersection_point(extra_ray2, segments)

        if closest_point:
            intersection_points.append(closest_point)
        if extra_closest_point1:
            extra_intersection_points.append(extra_closest_point1)
        if extra_closest_point2:
            extra_intersection_points.append(extra_closest_point2)

    # Sort intersection points by angle
    sorted_intersection_points = sort_intersection_points_by_angle(player,
                                                                   intersection_points + extra_intersection_points)

    draw_player(screen, player)

    # Draw the polygon onto the poly_surface with transparency
    poly_surface.fill((0, 0, 0, 200))  # Clear the surface
    draw_polygon(poly_surface, sorted_intersection_points, polygon_color)
    screen.blit(poly_surface, (0, 0))  # Blit the poly_surface onto the screen

    draw_polygon(poly_surface, sorted_intersection_points, polygon_color)

    pygame.display.flip()
    clock.tick(240)

pygame.quit()
sys.exit()



import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rain Effect")

# Colors
blue = (140, 180, 255)

# Wind speed (adjust as needed)
WIND_SPEED = -1  # Horizontal wind speed (leftward)

# Angle of rain tilt (in degrees)
RAIN_ANGLE = 95  # Adjust this angle to change the tilt of raindrops

# Convert angle to radians
ANGLE_RAD = math.radians(RAIN_ANGLE)

# Number of raindrops to appear per frame
RAIN_PER_FRAME = 3

# Raindrop class
class Raindrop:
    def __init__(self):
        self.x = random.randint(0, 1000)    # Random x position
        self.y = random.randint(-HEIGHT, 0)  # Random y position above the screen
        self.length = random.randint(5, 15)  # Length of the raindrop
        self.speed = random.randint(5, 15)   # Speed of the raindrop
        self.wind = WIND_SPEED               # Horizontal wind effect

    def fall(self):
        # Calculate new positions with tilt
        self.y += self.speed
        self.x += self.wind

        # Reset raindrop if it goes below the screen
        if self.y > HEIGHT:
            self.y = random.randint(-HEIGHT, 0)
            self.x = random.randint(0, 1000)

    def draw(self):
        # Calculate end position for tilted raindrop
        end_x = self.x + self.length * math.cos(ANGLE_RAD)
        end_y = self.y + self.length * math.sin(ANGLE_RAD)

        pygame.draw.line(screen, blue, (self.x, self.y), (end_x, end_y), 2)

# List to hold raindrops
raindrops = []
num_drops = 12
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Add new raindrops evenly over time
    if len(raindrops) < num_drops:
        for _ in range(RAIN_PER_FRAME):
            raindrops.append(Raindrop())

    # Clear screen
    screen.fill((0, 0, 0))

    # Update and draw raindrops
    for drop in raindrops:
        drop.fall()
        drop.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
