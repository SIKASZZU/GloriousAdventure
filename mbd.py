import pygame
from variables import UniversalVariables
from camera import Camera
import items
from loot import Loot


def update_object_dimensions():
    for item in items.items_list:
        if "Object_width" in item:
            item["Object_width"] = int(item["Object_width"] * UniversalVariables.block_size / items.block_size)
        if "Object_height" in item:
            item["Object_height"] = int(item["Object_height"] * UniversalVariables.block_size / items.block_size)

    items.block_size = UniversalVariables.block_size


def event_mousebuttondown(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            self.click_position = event.pos
            Camera.click_on_screen(self)

            Loot.loot_update(self)

            Camera.click_on_screen(self)

        #if UniversalVariables.debug_mode == True:
        if event.button == 4:  # Scroll +
            UniversalVariables.block_size += 10
            update_object_dimensions()

        elif event.button == 5:  # Scroll -
            UniversalVariables.block_size -= 10
            if UniversalVariables.block_size < 1:
                UniversalVariables.block_size = 1
            update_object_dimensions()
