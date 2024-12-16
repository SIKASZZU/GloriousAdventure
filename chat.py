import pygame
import sys
import time

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CHAT_WIDTH, CHAT_HEIGHT = 600, 300
CHAT_X, CHAT_Y = 100, 50
FONT_SIZE = 25
INPUT_HEIGHT = FONT_SIZE + 10
FPS = 30
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
ACTIVE_TEXT_COLOR = (0, 255, 0)  # Active suggestion color (e.g., bright green)
SHADOW_TEXT_COLOR = (100, 100, 100)  # Shadow suggestion color (e.g., gray)
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
start_index = 0  # To keep track of the starting index for displayed chat lines

# Chat box rects
chat_rect = pygame.Rect(CHAT_X, CHAT_Y, CHAT_WIDTH, CHAT_HEIGHT)
input_rect = pygame.Rect(CHAT_X, CHAT_Y + CHAT_HEIGHT, CHAT_WIDTH, INPUT_HEIGHT)


# Command functions
def command(command_name):
    print(f"{command_name} command.")


def help_command():
    for cmd, details in commands.items():
        chat_lines.append(cmd)


# Commands
commands = {
    '/hello': {
        'text': "Hello Command",
        'command': lambda: command("Hello")
    },
    '/goodbye': {
        'text': "Goodbye Command",
        'command': lambda: command("Goodbye")
    },
    '/fps': {
        'text': "FPS Command",
        'command': lambda: command("FPS")
    },
    '/time': {
        'text': "Time Command",
        'command': lambda: command("Time")
    },
    '/hitbox': {
        'text': "Hitbox Command",
        'command': lambda: command("Hitbox")
    },
    '/kill': {
        'text': "Kill Command",
        'command': lambda: command("Kill")
    },
    '/quit': {
        'text': "Quit Command",
        'command': lambda: command("Quit")
    },
    '/vision': {
        'text': "Vision Command",
        'command': lambda: command("Vision")
    },
    '/help': {
        'command': help_command
    },
    '/test': {
        'text': "Test",
    },
}


def draw_text(surface, text, pos, color):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)


def handle_command(command):
    global start_index
    command = command.lower()
    if command in commands:
        details = commands[command]

        if 'command' in details:
            details['command']()

        if 'text' in details:
            chat_lines.append(details['text'])
    else:
        chat_lines.append('Unknown command')
    # Scroll to the bottom when a new command is entered
    start_index = max(0, len(chat_lines) - (CHAT_HEIGHT // (FONT_SIZE + 5)) + 1)


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
                            # Scroll to the bottom when new text is added
                            start_index = max(0, len(chat_lines) - (CHAT_HEIGHT // (FONT_SIZE + 5)) + 1)
                        input_text = ""
                        last_input_time = current_time
                    chat_active = False
                    suggestions = []
                    suggestion_index = 0
                else:
                    chat_active = True
                    # Scroll to the bottom when the chat is activated
                    start_index = max(0, len(chat_lines) - (CHAT_HEIGHT // (FONT_SIZE + 5)) + 1)
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
            elif event.key == pygame.K_UP:
                if start_index > 0:
                    start_index -= 1  # Scroll up
            elif event.key == pygame.K_DOWN:
                if start_index < max(0, len(chat_lines) - (CHAT_HEIGHT // (FONT_SIZE + 5))):
                    start_index += 1  # Scroll down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Mouse wheel up
                if start_index > 0:
                    start_index -= 1  # Scroll up
            elif event.button == 5:  # Mouse wheel down
                if start_index < max(0, len(chat_lines) - (CHAT_HEIGHT // (FONT_SIZE + 5))):
                    start_index += 1  # Scroll down

    screen.fill(BG_COLOR)

    # Check if chat should be displayed
    if chat_active or current_time - last_input_time < CHAT_DISPLAY_DURATION:
        pygame.draw.rect(screen, CHAT_BG_COLOR, chat_rect)
        y = CHAT_Y + 10
        for line in chat_lines[start_index:start_index + (CHAT_HEIGHT // (FONT_SIZE + 5))]:
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
                start_y = CHAT_Y + CHAT_HEIGHT + 10

                # Handle cases based on the number of suggestions
                if num_suggestions == 1:
                    # When there's 1 suggestion, place it at spot 1 and shift other spots down
                    draw_text(screen, suggestions[suggestion_index], (CHAT_X + 10, start_y),
                              SHADOW_TEXT_COLOR)  # Active command in GRAY

                elif num_suggestions == 2:
                    # When there are 2 suggestions, place them at spots 1 and 2, shift 3rd spot down
                    draw_text(screen, suggestions[suggestion_index], (CHAT_X + 10, start_y),
                              SHADOW_TEXT_COLOR)  # Active suggestion in GRAY
                    draw_text(screen, suggestions[(suggestion_index + 1) % num_suggestions],
                              (CHAT_X + 10, start_y + FONT_SIZE + 5), TEXT_COLOR)

                else:
                    # When there are 3 or more suggestions, show them all without shifting
                    draw_text(screen, suggestions[suggestion_index], (CHAT_X + 10, start_y),
                              SHADOW_TEXT_COLOR)  # Active suggestion in GRAY
                    draw_text(screen, suggestions[(suggestion_index + 1) % num_suggestions],
                              (CHAT_X + 10, start_y + FONT_SIZE + 5), TEXT_COLOR)
                    draw_text(screen, suggestions[(suggestion_index + 2) % num_suggestions],
                              (CHAT_X + 10, start_y + 2 * (FONT_SIZE + 5)), TEXT_COLOR)

            # Input text
            draw_text(screen, input_text, (CHAT_X + 10, CHAT_Y + CHAT_HEIGHT + 10), text_color)

    pygame.display.flip()
    clock.tick(FPS)
