import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.text_fade_duration = 1000  # Duration of each fade in milliseconds
        self.text_elements = []  # Store text elements with their fade state

        # Player attributes
        self.player_x = 400
        self.player_y = 300
        self.player_speed = 5

        # FPS text element
        self.fps_text_position = (100, 100)

        # Text elements to be shown once
        self.ui_elements = [
            ("H - Show hitboxes", (400, 100)),
            ("J - Switch light", (400, 150)),
            ("Time: 12:00", (400, 250)),
            ("Day/Night: Day", (400, 300)),
        ]
        self.shown_texts = set()  # Track shown text elements

    def add_fading_text(self, text, position, color=(100, 255, 100)):
        """Add text to be rendered with a fading effect."""
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=position)
        start_time = pygame.time.get_ticks()
        self.text_elements.append((text_surface, text_rect, start_time, True))

    def handle_fading_texts(self):
        """Handle the fading effect for all text elements."""
        current_time = pygame.time.get_ticks()
        new_text_elements = []
        for surface, rect, start_time, fade_in in self.text_elements:
            elapsed_time = current_time - start_time
            if fade_in:
                if elapsed_time < self.text_fade_duration:
                    alpha = (elapsed_time / self.text_fade_duration) * 255
                    surface.set_alpha(alpha)
                    self.screen.blit(surface, rect)
                    new_text_elements.append((surface, rect, start_time, True))
                else:
                    # Start fading out
                    new_text_elements.append((surface, rect, current_time, False))
            else:
                if elapsed_time < self.text_fade_duration:
                    alpha = 255 - (elapsed_time / self.text_fade_duration) * 255
                    surface.set_alpha(alpha)
                    self.screen.blit(surface, rect)
                    new_text_elements.append((surface, rect, start_time, False))
                else:
                    # Fade out complete, do not re-add to new_text_elements
                    pass

        self.text_elements = new_text_elements

    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_x -= self.player_speed
        if keys[pygame.K_d]:
            self.player_x += self.player_speed
        if keys[pygame.K_w]:
            self.player_y -= self.player_speed
        if keys[pygame.K_s]:
            self.player_y += self.player_speed

    def render_player(self):
        pygame.draw.circle(self.screen, (255, 0, 0), (self.player_x, self.player_y), 20)

    def render_fps(self):
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (100, 255, 100))
        self.screen.blit(fps_text, self.fps_text_position)

    def render_general(self):
        for text, position in self.ui_elements:
            if text not in self.shown_texts:
                self.add_fading_text(text, position)
                self.shown_texts.add(text)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.handle_player_input()

            # Clear the screen
            self.screen.fill((0, 0, 0))

            self.render_general()
            self.render_player()
            self.render_fps()
            self.handle_fading_texts()

            # Update display
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
