import pygame
from variables import UniversalVariables
from camera import Camera
import items


def update_object_dimensions():
    for item in items.items_list:
        if "Object_width" in item:
            item["Object_width"] = int(item["Object_width"] * UniversalVariables.block_size / items.block_size)
        if "Object_height" in item:
            item["Object_height"] = int(item["Object_height"] * UniversalVariables.block_size / items.block_size)

    items.block_size = UniversalVariables.block_size  # Update block_size in items module


def event_mousebuttondown(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:

        if event.button == 1:  # Left mouse click
            self.click_position = event.pos  # window clicking reg.
            Camera.click_on_screen(self)

        elif event.button == 4:  # Scroll +
            UniversalVariables.block_size += 10  # Increase block_size

            UniversalVariables.player_height: int = UniversalVariables.block_size * 0.65
            UniversalVariables.player_width: int = UniversalVariables.block_size * 0.65

            UniversalVariables.player_hitbox_offset_x = 0.29 * UniversalVariables.player_height
            UniversalVariables.player_hitbox_offset_y = 0.22 * UniversalVariables.player_width
            update_object_dimensions()
        elif event.button == 5:  # Scroll -
            UniversalVariables.block_size -= 10  # Decrease block_size
            if UniversalVariables.block_size < 1:  # Prevent block_size from being less than 1
                UniversalVariables.block_size = 1

            UniversalVariables.player_height: int = UniversalVariables.block_size * 0.65
            UniversalVariables.player_width: int = UniversalVariables.block_size * 0.65

            UniversalVariables.player_hitbox_offset_x = 0.29 * UniversalVariables.player_height
            UniversalVariables.player_hitbox_offset_y = 0.22 * UniversalVariables.player_width
            update_object_dimensions()