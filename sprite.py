import pygame

### TODO: Kõik ümber teha, liiga raske animatsioone lisada, lic teha func millega on kegem animatsioone teha

def load_sprite_sheets(image_filenames):
    sprite_sheets = [pygame.image.load(filename).convert_alpha() for filename in image_filenames]
    animations = [[(0, 0, 130, 130)] * len(sprite_sheets) for _ in range(len(sprite_sheets))]
    return sprite_sheets, animations


class SpriteSheet:
    def __init__(self, image, variables):
        self.sheet = image
        self.variables = variables

    def get_image(self, x, y, width, height, filter_color=None):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))

        if filter_color:
            # Apply the filter color to non-transparent pixels
            for i in range(width):
                for j in range(height):
                    pixel_color = image.get_at((i, j))
                    if pixel_color[3] > 0:  # Check if the pixel is not transparent
                        filtered_color = (min(pixel_color[0] + filter_color[0], 255),
                                          min(pixel_color[1] + filter_color[1], 255),
                                          min(pixel_color[2] + filter_color[2], 255),
                                          pixel_color[3])
                        image.set_at((i, j), filtered_color)

        image = pygame.transform.scale(image, (self.variables.player_width, self.variables.player_height))
        return image


class AnimationManager:
    def __init__(self, sprite_sheets, animations, animation_speeds, variables):
        self.frame = None
        self.sprite_sheets = sprite_sheets
        self.animations = animations
        self.animation_speeds = animation_speeds
        self.animation_index = 3
        self.frame_index = 0
        self.animation_timer = 0
        self.variables = variables

    def update_animation(self, keys, is_idle):
        # Update animation index based on keys

        if not is_idle:
            if keys[pygame.K_a]:
                self.animation_index = 0  # Left animation
            elif keys[pygame.K_d]:
                self.animation_index = 1  # Right animation
            elif keys[pygame.K_w]:
                self.animation_index = 2  # Up animation
            elif keys[pygame.K_s]:
                self.animation_index = 3  # Down animation
        elif is_idle:
            if self.variables.last_input == "a":
                self.animation_index = 0  # Left animation
            elif self.variables.last_input == "d":
                self.animation_index = 1  # Right animation
            elif self.variables.last_input == "w":
                self.animation_index = 2  # Up animation
            elif self.variables.last_input == "s":
                self.animation_index = 3  # Down animation
            self.variables.last_input = 'None'  # resetin selle 2ra, sest niisama tra. lheb vist vaja. fuck you 20.11.24

        # Update animation frame based on animation_timer and animation_speed
        self.animation_timer += 1
        sprite_sheet = SpriteSheet(self.sprite_sheets[self.animation_index], self.variables)
        x, y, animation_width, animation_height = self.animations[self.animation_index][0]
        if self.variables.health_status == True:
            self.frame = sprite_sheet.get_image(x + self.frame_index * animation_width, y, animation_width,
                                                animation_height, filter_color=(0, 255, 0))
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.animation_index])
            self.animation_timer = 0  # Reset the animation timer
            self.variables.health_status = None

            return self.frame

        elif self.variables.health_status == False:
            self.frame = sprite_sheet.get_image(x + self.frame_index * animation_width, y, animation_width,
                                                animation_height, filter_color=(255, 0, 0))
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.animation_index])
            self.animation_timer = 0  # Reset the animation timer
            self.variables.health_status = None

            return self.frame

        elif self.animation_timer >= self.animation_speeds[self.animation_index]:
            self.frame = sprite_sheet.get_image(x + self.frame_index * animation_width, y, animation_width,
                                                animation_height)
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.animation_index])
            self.animation_timer = 0  # Reset the animation timer

            return self.frame

        # If no frame change, return the current frame
        else:
            self.frame = sprite_sheet.get_image(x + self.frame_index * animation_width, y, animation_width, animation_height)
            return self.frame
