import pygame
import sys
import time

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CHAT_WIDTH, CHAT_HEIGHT = 600, 300
CHAT_X, CHAT_Y = 100, 50
FONT_SIZE = 25
INPUT_HEIGHT = 50
FPS = 30
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
ACTIVE_TEXT_COLOR = (0, 255, 0)  # Active suggestion color (e.g., bright green)
SHADOW_TEXT_COLOR = (100, 100, 100)  # Active suggestion color (e.g., bright green)
INPUT_COLOR = (50, 50, 50)
INPUT_TEXT_COLOR = (255, 255, 255)
CHAT_BG_COLOR = (40, 40, 40)
CHAT_DISPLAY_DURATION = 5  # seconds

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Chat")
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, FONT_SIZE)

# Chat variables
chat_lines = []
input_text = ""
chat_active = False
last_input_time = 0
suggestion_index = 0
suggestions = []

# Chat box rects
chat_rect = pygame.Rect(CHAT_X, CHAT_Y, CHAT_WIDTH, CHAT_HEIGHT)
input_rect = pygame.Rect(CHAT_X, CHAT_Y + CHAT_HEIGHT - INPUT_HEIGHT, CHAT_WIDTH, INPUT_HEIGHT)


# Command functions
def command(command_name):
    print(f"{command_name} command.")

def help_command():
    for item in commands:
        chat_lines.append(item)

# Commands
commands = {
    '/hello': ("Hello Command", lambda: command("Hello")),
    '/goodbye': ("Goodbye Command", lambda: command("Goodbye")),
    '/fps': ("FPS Command", lambda: command("FPS")),
    '/time': ("Time Command", lambda: command("Time")),
    '/hitbox': ("Hitbox Command", lambda: command("Hitbox")),
    '/kill': ("Kill Command", lambda: command("Kill")),
    '/quit': ("Quit Command", lambda: command("Quit")),
    '/vision': ("Vision Command", lambda: command("Vision")),
    '/help': ("", help_command),
}



def draw_text(surface, text, pos, color):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)


def handle_command(command):
    command = command.lower()
    if command in commands:
        message, command_function = commands[command]
        command_function()
        chat_lines.append(message)
    else:
        chat_lines.append('Unknown command')


def get_command_suggestions(command_prefix):
    return [cmd for cmd in commands if cmd.startswith(command_prefix)]  # All matching commands


while True:
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if chat_active:
                    if input_text:
                        if input_text.startswith('/'):
                            handle_command(input_text)
                        else:
                            chat_lines.append(input_text)
                        input_text = ""
                        last_input_time = current_time
                    chat_active = False
                    suggestions = []
                    suggestion_index = 0
                else:
                    chat_active = True
            elif event.key == pygame.K_TAB and chat_active:
                if input_text.startswith('/'):
                    if not suggestions:
                        suggestions = get_command_suggestions(input_text)
                    if suggestions:
                        # Insert the current suggestion into input_text
                        suggestion_index = (suggestion_index + 1) % len(suggestions)  # Cycle through suggestions
                        input_text = suggestions[suggestion_index]
                    else:
                        suggestions = []  # Reset suggestions if no matching commands
            elif chat_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    # Reset suggestions on deletion
                    suggestions = get_command_suggestions(input_text) if input_text.startswith('/') else []
                    suggestion_index = 0  # Reset suggestion index when backspacing
                else:
                    input_text += event.unicode
                    # Reset suggestions when typing
                    suggestions = get_command_suggestions(input_text) if input_text.startswith('/') else []
                    suggestion_index = 0  # Reset suggestion index when typing

    screen.fill(BG_COLOR)

    # Check if chat should be displayed
    if chat_active or current_time - last_input_time < CHAT_DISPLAY_DURATION:
        pygame.draw.rect(screen, CHAT_BG_COLOR, chat_rect)
        y = CHAT_Y + 10
        for line in chat_lines[-(CHAT_HEIGHT // (FONT_SIZE + 5)) + 1:]:
            draw_text(screen, line, (CHAT_X + 10, y), TEXT_COLOR)
            y += FONT_SIZE + 5

        if chat_active:
            pygame.draw.rect(screen, INPUT_COLOR, input_rect)

            if input_text.startswith('/'):
                text_color = ACTIVE_TEXT_COLOR
            else:
                text_color = INPUT_TEXT_COLOR

            # Handle displaying suggestions based on available suggestions
            if input_text.startswith('/') and suggestions:
                # Get the number of available suggestions
                num_suggestions = len(suggestions)

                # Calculate the starting Y position for the suggestions
                start_y = CHAT_Y + CHAT_HEIGHT - INPUT_HEIGHT - FONT_SIZE - 5 - INPUT_HEIGHT * 1.2

                # Handle cases based on the number of suggestions
                if num_suggestions == 1:
                    # When there's 1 suggestion, place it at spot 1 and shift other spots down
                    draw_text(screen, suggestions[suggestion_index], (CHAT_X + 10, CHAT_Y + CHAT_HEIGHT - INPUT_HEIGHT + 10), SHADOW_TEXT_COLOR)  # Active command in GRAY

                elif num_suggestions == 2:
                    # When there are 2 suggestions, place them at spots 1 and 2, shift 3rd spot down
                    for i, suggestion in enumerate(suggestions[suggestion_index:suggestion_index + 2]):
                        if i == 0:
                            draw_text(screen, suggestion, (CHAT_X + 10, CHAT_Y + CHAT_HEIGHT - INPUT_HEIGHT + 10), SHADOW_TEXT_COLOR)  # Active suggestion in GRAY

                        else:
                            draw_text(screen, suggestion, (CHAT_X + 10, CHAT_Y + CHAT_HEIGHT + 10 + (i - 1) * (FONT_SIZE + 5)), TEXT_COLOR)

                else:
                    # When there are 3 or more suggestions, show them all without shifting
                    for i, suggestion in enumerate(suggestions[suggestion_index:suggestion_index + 3]):
                        if i == 0:
                            draw_text(screen, suggestion, (CHAT_X + 10, CHAT_Y + CHAT_HEIGHT - INPUT_HEIGHT + 10), SHADOW_TEXT_COLOR)  # Active suggestion in GRAY

                        else:

                            draw_text(screen, suggestion, (CHAT_X + 10, CHAT_Y + CHAT_HEIGHT + 10 + (i - 1) * (FONT_SIZE + 5)), TEXT_COLOR)

            # Input text - Mida me ise kirjutame
            draw_text(screen, input_text, (CHAT_X + 10, CHAT_Y + CHAT_HEIGHT - INPUT_HEIGHT + 10), text_color)


    pygame.display.flip()
    clock.tick(FPS)
