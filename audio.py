import random

import pygame
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Player_audio:

    def __init__(self, terrain_data, player, py_mixer, variables):
        self.terrain_data = terrain_data
        self.player = player
        self.py_mixer = py_mixer
        self.mixer = pygame.mixer
        self.variables = variables

        self.previous_ground_sound = None

        # Load sounds with resource_path
        self.player_hit_sound = self.mixer.Sound(resource_path('audio/Player_Sounds/Player_Got_Hurt.wav'))
        self.player_death_sound = self.mixer.Sound(resource_path('audio/Player_Sounds/Player_Died.wav'))

        self.maze_ground_sound = self.mixer.Sound(resource_path('audio/Tile_Sounds/Maze_Ground_Sound.wav'))
        self.water_sound = self.mixer.Sound(resource_path('audio/Tile_Sounds/Water_Sound.mp3'))

        self.in_range_click_sound = self.mixer.Sound(resource_path('audio/Event_Sounds/In_Range_Click_Sound.mp3'))
        self.out_of_range_click_sound = self.mixer.Sound(resource_path('audio/Event_Sounds/Out_Of_Range_Click_Sound.mp3'))
        self.item_sound = self.mixer.Sound(resource_path('audio/Event_Sounds/Item_Sound.mp3'))
        self.error_sound = self.mixer.Sound(resource_path('audio/Event_Sounds/Error_Sound.mp3'))
        self.cant_open_a_barrel_sound = self.mixer.Sound(resource_path('audio/Event_Sounds/Cant_Open_A_Barrel.mp3'))
        self.eating_sound = self.mixer.Sound(resource_path('audio/Event_Sounds/Eating_Sound.mp3'))
        self.drinking_sound = self.mixer.Sound(resource_path('audio/Event_Sounds/Drinking_Sound.mp3'))
        self.ghost_hurt = self.mixer.Sound(resource_path('audio/Ghost_Sounds/Ghost_Hurt.mp3'))
        self.ghost_died = self.mixer.Sound(resource_path('audio/Ghost_Sounds/Ghost_Died.mp3'))

        self.opening_a_barrel_sounds = [
            self.mixer.Sound(resource_path('audio/Event_Sounds/Opening_A_Barrel_0.mp3')),
            self.mixer.Sound(resource_path('audio/Event_Sounds/Opening_A_Barrel_1.mp3')),
            self.mixer.Sound(resource_path('audio/Event_Sounds/Opening_A_Barrel_2.mp3')),

        ]


        # Preload sounds for ground, trees, rocks, etc.
        self.grass_sounds = [
            self.mixer.Sound(resource_path('audio/Tile_Sounds/Grass_Left_Foot_Sound.mp3')),
            self.mixer.Sound(resource_path('audio/Tile_Sounds/Grass_Right_Foot_Sound.mp3')),
        ]
        self.current_grass_sound_index = 0

        self.grass_channel = self.mixer.Channel(1)  # Seob 1. channeli groundiga
        self.water_channel = self.mixer.Channel(2)  # Seob 2. channeli veega
        self.maze_channel = self.mixer.Channel(3)  # Seob 3. channeli maze'iga

        self.player_channel = self.mixer.Channel(4)  # Seob 4. channeli playeriga
        self.event_channel = self.mixer.Channel(5)  # Seob 3. channeli maze'iga

        self.death_counter = 0
        self.current_health: int = None

        self.water_sound_list: list[int, ...] = [0]
        self.ground_sound_list: list[int, ...] = [1, 2, 4, 7, 107]
        self.maze_ground_list: list[int, ...] = [11, 89, 90, 91, 92, 93, 933, 94, 95, 96, 97, 977, 98, 988, 99]
        self.audio_list: list[str, ...] = [
            # Player
            self.player_death_sound, self.player_hit_sound,

            # Events
            self.in_range_click_sound, self.out_of_range_click_sound, self.item_sound, self.error_sound,
            self.opening_a_barrel_sounds, self.cant_open_a_barrel_sound, self.eating_sound,

            # Tiles
            self.water_sound, self.maze_ground_sound,
            self.grass_sounds,

            # entity
            self.ghost_hurt, self.ghost_died,
        ]

        for audio_name in self.audio_list:
            if type(audio_name) == list:
                for sound in audio_name:
                    sound.set_volume(0.0)
                    sound.play()
                    sound.stop()
                    sound.set_volume(self.variables.sound_volume)

            else:
                audio_name.set_volume(0.0)
                audio_name.play()
                audio_name.stop()

                # Muudab kogu mängu audio ära vastavalt sound_volume'ile
                audio_name.set_volume(self.variables.sound_volume)

    def player_movement_audio(self) -> None:
        player_grid_x = int(self.variables.player_x // self.variables.block_size)
        player_grid_y = int(self.variables.player_y // self.variables.block_size)
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte
        try:

            if keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d] or keys[pygame.K_w]:
                if self.terrain_data[player_grid_y][player_grid_x] in self.ground_sound_list:
                    if not self.grass_channel.get_busy():
                        self.grass_channel.play(
                            self.grass_sounds[self.current_grass_sound_index])
                        self.current_grass_sound_index = (self.current_grass_sound_index + 1) % len(
                            self.grass_sounds)

                    # Kaotab muud liikumise helid ära, mis seonduvad player'iga
                    if self.water_channel.get_busy():
                        self.water_channel.stop()
                    if self.maze_channel.get_busy():
                        self.maze_channel.stop()

                elif self.terrain_data[player_grid_y][player_grid_x] in self.water_sound_list:
                    if not self.water_channel.get_busy():
                        self.water_channel.play(self.water_sound)

                    # Kaotab muud liikumise helid ära, mis seonduvad player'iga
                    if self.grass_channel.get_busy():
                        self.grass_channel.stop()
                    if self.maze_channel.get_busy():
                        self.maze_channel.stop()

                elif self.terrain_data[player_grid_y][player_grid_x] in self.maze_ground_list:
                    if not self.maze_channel.get_busy():
                        self.maze_channel.play(self.maze_ground_sound)

                    # Kaotab muud liikumise helid ära, mis seonduvad player'iga
                    if self.grass_channel.get_busy():
                        self.grass_channel.stop()
                    if self.water_channel.get_busy():
                        self.water_channel.stop()

                else:
                    # Kaotab kõik liikumisega seonduvad helid ära kui player ei liigu
                    if self.grass_channel.get_busy():
                        self.grass_channel.stop()
                    if self.water_channel.get_busy():
                        self.water_channel.stop()
                    if self.maze_channel.get_busy():
                        self.maze_channel.stop()

            else:
                # Kaotab kõik liikumisega seonduvad helid ära kui player ei liigu
                if self.grass_channel.get_busy():
                    self.grass_channel.stop()
                if self.water_channel.get_busy():
                    self.water_channel.stop()
                if self.maze_channel.get_busy():
                    self.maze_channel.stop()

        except IndexError or TypeError:

            # Kaotab kõik liikumisega seonduvad helid ära kui tuleb error
            if self.grass_channel.get_busy():
                self.grass_channel.stop()
            if self.water_channel.get_busy():
                self.water_channel.stop()
            if self.maze_channel.get_busy():
                self.maze_channel.stop()

            return

    def player_hurt_audio(self) -> None:
        # Kui current health puudub siis muudab selle playeri eludeks, mis tal hetkel oli
        if self.current_health is None:
            self.current_health = self.player.health.get_health()

        # Kui playeri kaotab elusi siis käid 'Player_hit' heli
        if self.current_health > self.player.health.get_health() > 0:

            self.player_channel.play(self.player_hit_sound)
            self.current_health = self.player.health.get_health()

        else:
            return

    def player_death_audio(self) -> None:
        if self.player.health.get_health() <= 0 and self.death_counter == 0:

            if self.player_channel.get_busy():
                self.player_channel.stop()

            self.player_channel.play(self.player_death_sound)
            self.death_counter += 1

        else:
            return

    def player_click_audio(self, range) -> None:
        if self.get_busy():
            self.stop()

        if range:
            self.event_channel.play(self.in_range_click_sound)
        else:
            self.event_channel.play(self.out_of_range_click_sound)

    def player_item_audio(self) -> None:
        if self.event_channel.get_busy():
            self.event_channel.stop()
        self.event_channel.play(self.item_sound)

    def error_audio(self) -> None:
        if self.event_channel.get_busy():
            self.event_channel.stop()
        self.event_channel.play(self.error_sound)

    def opening_a_barrel_audio(self, able=True):
        if self.event_channel.get_busy():
            self.event_channel.stop()

        if able:
            self.event_channel.play(random.choice(self.opening_a_barrel_sounds))
        else:
            self.event_channel.play(self.cant_open_a_barrel_sound)

    def eating_audio(self) -> None:
        if self.event_channel.get_busy():
            self.event_channel.stop()
        self.event_channel.play(self.eating_sound)

    def drinking_audio(self) -> None:
        if self.event_channel.get_busy():
            self.event_channel.stop()
        self.event_channel.play(self.drinking_sound)

    def ghost_hurt_audio(self) -> None:
        if self.event_channel.get_busy():
            self.event_channel.stop()
        self.event_channel.play(self.ghost_hurt)

    def ghost_died_audio(self) -> None:
        if self.event_channel.get_busy():
            self.event_channel.stop()
        self.event_channel.play(self.ghost_died)
    
    def player_audio_update(self) -> None:
        self.player_movement_audio()
        self.player_hurt_audio()
        self.player_death_audio()


class Tile_Sounds:
    def __init__(self, py_mixer, variables):
        self.py_mixer = py_mixer
        self.mixer    = pygame.mixer
        self.variables = variables

        self.insert_key_sound = self.mixer.Sound(resource_path('audio/Tile_Sounds/Key_To_Slot.mp3'))
        self.pop_key_sound = self.mixer.Sound(resource_path('audio/Tile_Sounds/Key_From_Slot.mp3'))
        self.portal_open_sound = self.mixer.Sound(resource_path('audio/Tile_Sounds/Portal_Open_Sound.mp3'))
        self.portal_close_sound = self.mixer.Sound(resource_path('audio/Tile_Sounds/Portal_Close_Sound.mp3'))

        self.key_channel = self.mixer.Channel(6)
        self.portal_channel = self.mixer.Channel(7)

        self.audio_list = [self.insert_key_sound, self.pop_key_sound, self.portal_open_sound, self.portal_close_sound]

        for audio_name in self.audio_list:
            audio_name.set_volume(0.0)
            audio_name.play()
            audio_name.stop()

            # Muudab kogu mängu audio ära vastavalt sound_volume'ile
            audio_name.set_volume(self.variables.sound_volume)

    def portal_open_audio(self) -> None:
        if self.portal_channel.get_busy():
            self.portal_channel.stop()

        self.portal_channel.play(self.portal_open_sound)

    def portal_close_audio(self) -> None:
        if self.portal_channel.get_busy():
            self.portal_channel.stop()

        self.portal_channel.play(self.portal_close_sound)

    def insert_key_audio(self) -> None:
        if self.key_channel.get_busy():
            self.key_channel.stop()

        self.key_channel.play(self.insert_key_sound)

    def pop_key_audio(self) -> None:
        if self.key_channel.get_busy():
            self.key_channel.stop()

        self.key_channel.play(self.pop_key_sound)
