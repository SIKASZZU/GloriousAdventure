import pygame

from variables import UniversalVariables
from objects import ObjectManagement
from audio import Player_audio
from camera import Camera
class Build:

    def is_valid_item(self):
        # Vaatab kas equiped item on placeable kui on siis return True
        ...

    def is_valid_location(self):
        # Vaatab kas valitud koht on valid --- self.terrain_data[][] == 1, peab olema ka player range'is
        ...

    def update(self):
        # Update loogika järjekord
        ...
