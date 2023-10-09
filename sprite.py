import pygame

def load_sprite_sheets(image_filenames):
    sprite_sheets = [pygame.image.load(filename).convert_alpha() for filename in image_filenames]
    animations = [[(0, 0, 130, 130)] * len(sprite_sheets) for _ in range(len(sprite_sheets))]
    return sprite_sheets, animations

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

        self.block_size = 100

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (self.block_size, self.block_size))
        return image


class AnimationManager:
    def __init__(self, sprite_sheets, animations, animation_speeds):
        self.frame = None
        self.sprite_sheets = sprite_sheets
        self.animations = animations
        self.animation_speeds = animation_speeds
        self.animation_index = 3
        self.frame_index = 0
        self.animation_timer = 0

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

        # Update animation frame based on animation_timer and animation_speed
        self.animation_timer += 1
        sprite_sheet = SpriteSheet(self.sprite_sheets[self.animation_index])
        x, y, animation_width, animation_height = self.animations[self.animation_index][0]

        if self.animation_timer >= self.animation_speeds[self.animation_index]:
            self.frame = sprite_sheet.get_image(x + self.frame_index * animation_width, y, animation_width, animation_height)
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.animation_index])
            self.animation_timer = 0  # Reset the animation timer

            return self.frame

        # If no frame change, return the current frame
        else:
            return sprite_sheet.get_image(x + self.frame_index * animation_width, y, animation_width, animation_height)




