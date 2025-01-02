import pygame
import textwrap

from variables import UniversalVariables

class Fading_text:
    def __init__(self, screen, variables):
        self.screen = screen
        self.variables = variables
            
        self.shown_texts = set()
        self.text_fade_duration = 700  # Duration of each fade in milliseconds
        self.text_elements = []  # Store text elements with their fade state

    def update(self):
        self.render_general()
        self.handle_fading_texts()
        self.variables.screen.blits(self.variables.text_sequence)

    def render_general(self):
        for text in self.variables.ui_elements:
            if text not in self.shown_texts:
                self.add_fading_text(text)
                self.shown_texts.add(text)


    def add_fading_text(self, text, color=(255, 255, 255), background_color=(30, 30, 30), padding=5):
        """Add text with a background to be rendered with a fading effect."""
        max_width = self.variables.screen_x  # Max width with padding
        # Start with a relatively large font size
        font_size = 20
        font = pygame.font.SysFont("Verdana", font_size)
        lines = textwrap.wrap(text, width=max_width // font_size)

        # Decrease font size until the text fits within the screen bounds
        while True:
            text_surfaces = []
            text_rects = []

            for line in lines:
                text_surface = font.render(line, True, color)
                text_rect = text_surface.get_rect()
                text_surfaces.append(text_surface)
                text_rects.append(text_rect)

            total_height = sum(rect.height for rect in text_rects) + (len(text_rects) - 1) * padding
            if total_height < self.variables.screen_y * 0.9:
                break
            else:
                font_size -= 1
                font = pygame.font.SysFont("Verdana", font_size)
                lines = textwrap.wrap(text, width=max_width // font_size)

        # Position the text so that its bottom aligns with self.variables.screen_y * 0.9
        start_y = self.variables.screen_y * 0.88 - total_height

        # Calculate the total width and height for the background surface
        max_text_width = max(text_rect.width for text_rect in text_rects)
        background_surface = pygame.Surface((max_text_width + 2 * padding, total_height + 2 * padding), pygame.SRCALPHA)
        pygame.draw.rect(background_surface, background_color, background_surface.get_rect(), border_radius=20)
        background_surface.set_alpha(100)  # Set transparency to 100

        # Center the background surface on the screen
        background_rect = background_surface.get_rect(
            center=(self.variables.screen_x // 2, start_y + total_height // 2))

        # Center text lines within the background surface
        current_y = padding
        for text_surface, text_rect in zip(text_surfaces, text_rects):
            text_rect.topleft = (padding, current_y)
            current_y += text_rect.height + padding

        # Create a list of tuples with the background surface, its rect, and the text surfaces with their rects
        start_time = pygame.time.get_ticks()
        duration = len(text) * 0.05 * 1000  # Duration based on text length

        # Remove the currently displayed text element, if any
        self.text_elements = []

        self.text_elements.append(
            (background_surface, background_rect, text_surfaces, text_rects, start_time, True, duration))


    def handle_fading_texts(self):
        """Handle the fading effect for all text elements."""
        current_time = pygame.time.get_ticks()
        new_text_elements = []
        for background_surface, background_rect, text_surfaces, text_rects, start_time, fade_in, duration in self.text_elements:
            elapsed_time = current_time - start_time
            if fade_in:
                if elapsed_time < 500:  # Fade in for 0.5 seconds
                    alpha = (elapsed_time / 500) * 255
                elif elapsed_time < duration + 500:  # Stay at full opacity for text length * 0.05 seconds
                    alpha = 255
                elif elapsed_time < duration + 1000:  # Fade out for 0.5 seconds
                    alpha = 255 - ((elapsed_time - (duration + 500)) / 500) * 255
                else:
                    continue  # Fade out complete, do not re-add to new_text_elements

                # Blit the background once
                background_surface.set_alpha(min(alpha, 100))  # Limit alpha to 100
                self.screen.blit(background_surface, background_rect)

                # Blit each line of text
                for text_surface, text_rect in zip(text_surfaces, text_rects):
                    text_surface.set_alpha(min(alpha, 255))  # Limit alpha to 255 for text
                    centered_text_rect = text_rect.copy()
                    centered_text_rect.centerx = background_rect.centerx
                    centered_text_rect.top = background_rect.top + text_rect.top
                    self.screen.blit(text_surface, centered_text_rect.topleft)

                new_text_elements.append(
                    (background_surface, background_rect, text_surfaces, text_rects, start_time, True, duration))
            else:
                if elapsed_time < 500:  # Fade out for 0.5 seconds
                    alpha = 255 - (elapsed_time / 500) * 255
                else:
                    continue  # Fade out complete, do not re-add to new_text_elements

                # Blit the background once
                background_surface.set_alpha(min(alpha, 100))  # Limit alpha to 100
                self.screen.blit(background_surface, background_rect)

                # Blit each line of text
                for text_surface, text_rect in zip(text_surfaces, text_rects):
                    text_surface.set_alpha(min(alpha, 255))  # Limit alpha to 255 for text
                    centered_text_rect = text_rect.copy()
                    centered_text_rect.centerx = background_rect.centerx
                    centered_text_rect.top = background_rect.top + text_rect.top
                    self.screen.blit(text_surface, centered_text_rect.topleft)

                new_text_elements.append(
                    (background_surface, background_rect, text_surfaces, text_rects, start_time, False, duration))

        self.text_elements = new_text_elements

    def re_display_fading_text(self, text: str, debug: bool = False) -> None:
        # Kui debug = True, disply'b text'i ainult siis kui debug_mode = True
        if debug and not self.variables.debug_mode:
            return

        self.variables.ui_elements.append(text)
        if text in self.shown_texts:
            self.shown_texts.remove(text)

    def display_once_fading_text(self, text: str) -> None:
        if text in self.shown_texts:
            return
        self.variables.ui_elements.append(text)