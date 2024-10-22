import random

import pygame
import os
import sys

from variables import UniversalVariables


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Player_audio:
    # Initialize pygame
    pygame.mixer.init()

    previous_ground_sound = None

    # Load sounds with resource_path
    player_hit_sound = pygame.mixer.Sound(resource_path('audio/Player_Sounds/Player_Got_Hurt.wav'))
    player_death_sound = pygame.mixer.Sound(resource_path('audio/Player_Sounds/Player_Died.wav'))

    maze_ground_sound = pygame.mixer.Sound(resource_path('audio/Tile_Sounds/Maze_Ground_Sound.wav'))
    water_sound = pygame.mixer.Sound(resource_path('audio/Tile_Sounds/Water_Sound.mp3'))

    in_range_click_sound = pygame.mixer.Sound(resource_path('audio/Event_Sounds/In_Range_Click_Sound.mp3'))
    out_of_range_click_sound = pygame.mixer.Sound(resource_path('audio/Event_Sounds/Out_Of_Range_Click_Sound.mp3'))
    item_sound = pygame.mixer.Sound(resource_path('audio/Event_Sounds/Item_Sound.mp3'))
    error_sound = pygame.mixer.Sound(resource_path('audio/Event_Sounds/Error_Sound.mp3'))
    cant_open_a_barrel_sound = pygame.mixer.Sound(resource_path('audio/Event_Sounds/Cant_Open_A_Barrel.mp3'))
    eating_sound = pygame.mixer.Sound(resource_path('audio/Event_Sounds/Eating_Sound.mp3'))
    drinking_sound = pygame.mixer.Sound(resource_path('audio/Event_Sounds/Drinking_Sound.mp3'))
    ghost_hurt = pygame.mixer.Sound(resource_path('audio/Ghost_Sounds/Ghost_Hurt.mp3'))
    ghost_died = pygame.mixer.Sound(resource_path('audio/Ghost_Sounds/Ghost_Died.mp3'))

    opening_a_barrel_sounds = [
        pygame.mixer.Sound(resource_path('audio/Event_Sounds/Opening_A_Barrel_0.mp3')),
        pygame.mixer.Sound(resource_path('audio/Event_Sounds/Opening_A_Barrel_1.mp3')),
        pygame.mixer.Sound(resource_path('audio/Event_Sounds/Opening_A_Barrel_2.mp3')),

    ]


    # Preload sounds for ground, trees, rocks, etc.
    grass_sounds = [
        pygame.mixer.Sound(resource_path('audio/Tile_Sounds/Grass_Left_Foot_Sound.mp3')),
        pygame.mixer.Sound(resource_path('audio/Tile_Sounds/Grass_Right_Foot_Sound.mp3')),
    ]
    current_grass_sound_index = 0

    grass_channel = pygame.mixer.Channel(1)  # Seob 1. channeli groundiga
    water_channel = pygame.mixer.Channel(2)  # Seob 2. channeli veega
    maze_channel = pygame.mixer.Channel(3)  # Seob 3. channeli maze'iga

    player_channel = pygame.mixer.Channel(4)  # Seob 4. channeli playeriga
    event_channel = pygame.mixer.Channel(5)  # Seob 3. channeli maze'iga

    death_counter = 0
    current_health: int = None

    water_sound_list: list[int, ...] = [0]
    ground_sound_list: list[int, ...] = [1, 2, 4, 7, 107]
    maze_ground_list: list[int, ...] = [11, 89, 90, 91, 92, 93, 933, 94, 95, 96, 97, 977, 98, 988, 99]
    audio_list: list[str, ...] = [
        # Player
        player_death_sound, player_hit_sound,

        # Events
        in_range_click_sound, out_of_range_click_sound, item_sound, error_sound,
        opening_a_barrel_sounds, cant_open_a_barrel_sound, eating_sound,

        # Tiles
        water_sound, maze_ground_sound,
        grass_sounds]

    for audio_name in audio_list:
        if type(audio_name) == list:
            for sound in audio_name:
                sound.set_volume(0.0)
                sound.play()
                sound.stop()
                sound.set_volume(UniversalVariables.sound_volume)

        else:
            audio_name.set_volume(0.0)
            audio_name.play()
            audio_name.stop()

            # Muudab kogu mängu audio ära vastavalt sound_volume'ile
            audio_name.set_volume(UniversalVariables.sound_volume)

    def __init__(self):
        self.terrain_data = None
        self.player = None

    def player_movement_audio(self) -> None:
        player_grid_x = int(UniversalVariables.player_x // UniversalVariables.block_size)
        player_grid_y = int(UniversalVariables.player_y // UniversalVariables.block_size)
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte
        try:

            if keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d] or keys[pygame.K_w]:
                if self.terrain_data[player_grid_y][player_grid_x] in Player_audio.ground_sound_list:
                    if not Player_audio.grass_channel.get_busy():
                        Player_audio.grass_channel.play(
                            Player_audio.grass_sounds[Player_audio.current_grass_sound_index])
                        Player_audio.current_grass_sound_index = (Player_audio.current_grass_sound_index + 1) % len(
                            Player_audio.grass_sounds)

                    # Kaotab muud liikumise helid ära, mis seonduvad player'iga
                    if Player_audio.water_channel.get_busy():
                        Player_audio.water_channel.stop()
                    if Player_audio.maze_channel.get_busy():
                        Player_audio.maze_channel.stop()

                elif self.terrain_data[player_grid_y][player_grid_x] in Player_audio.water_sound_list:
                    if not Player_audio.water_channel.get_busy():
                        Player_audio.water_channel.play(Player_audio.water_sound)

                    # Kaotab muud liikumise helid ära, mis seonduvad player'iga
                    if Player_audio.grass_channel.get_busy():
                        Player_audio.grass_channel.stop()
                    if Player_audio.maze_channel.get_busy():
                        Player_audio.maze_channel.stop()

                elif self.terrain_data[player_grid_y][player_grid_x] in Player_audio.maze_ground_list:
                    if not Player_audio.maze_channel.get_busy():
                        Player_audio.maze_channel.play(Player_audio.maze_ground_sound)

                    # Kaotab muud liikumise helid ära, mis seonduvad player'iga
                    if Player_audio.grass_channel.get_busy():
                        Player_audio.grass_channel.stop()
                    if Player_audio.water_channel.get_busy():
                        Player_audio.water_channel.stop()

                else:
                    # Kaotab kõik liikumisega seonduvad helid ära kui player ei liigu
                    if Player_audio.grass_channel.get_busy():
                        Player_audio.grass_channel.stop()
                    if Player_audio.water_channel.get_busy():
                        Player_audio.water_channel.stop()
                    if Player_audio.maze_channel.get_busy():
                        Player_audio.maze_channel.stop()

            else:
                # Kaotab kõik liikumisega seonduvad helid ära kui player ei liigu
                if Player_audio.grass_channel.get_busy():
                    Player_audio.grass_channel.stop()
                if Player_audio.water_channel.get_busy():
                    Player_audio.water_channel.stop()
                if Player_audio.maze_channel.get_busy():
                    Player_audio.maze_channel.stop()

        except IndexError or TypeError:

            # Kaotab kõik liikumisega seonduvad helid ära kui tuleb error
            if Player_audio.grass_channel.get_busy():
                Player_audio.grass_channel.stop()
            if Player_audio.water_channel.get_busy():
                Player_audio.water_channel.stop()
            if Player_audio.maze_channel.get_busy():
                Player_audio.maze_channel.stop()

            return

    def player_hurt_audio(self) -> None:
        # Kui current health puudub siis muudab selle playeri eludeks, mis tal hetkel oli
        if Player_audio.current_health is None:
            Player_audio.current_health = self.player.health.get_health()

        # Kui playeri kaotab elusi siis käid 'Player_hit' heli
        if Player_audio.current_health > self.player.health.get_health() > 0:

            Player_audio.player_channel.play(Player_audio.player_hit_sound)
            Player_audio.current_health = self.player.health.get_health()

        else:
            return

    def player_death_audio(self) -> None:
        if self.player.health.get_health() <= 0 and Player_audio.death_counter == 0:

            if Player_audio.player_channel.get_busy():
                Player_audio.player_channel.stop()

            Player_audio.player_channel.play(Player_audio.player_death_sound)
            Player_audio.death_counter += 1

        else:
            return

    def player_click_audio(self, range) -> None:
        if Player_audio.event_channel.get_busy():
            Player_audio.event_channel.stop()

        if range:
            Player_audio.event_channel.play(Player_audio.in_range_click_sound)
        else:
            Player_audio.event_channel.play(Player_audio.out_of_range_click_sound)

    def player_item_audio(self) -> None:
        if Player_audio.event_channel.get_busy():
            Player_audio.event_channel.stop()
        Player_audio.event_channel.play(Player_audio.item_sound)

    def error_audio(self) -> None:
        if Player_audio.event_channel.get_busy():
            Player_audio.event_channel.stop()
        Player_audio.event_channel.play(Player_audio.error_sound)

    def opening_a_barrel_audio(self, able=True):
        if Player_audio.event_channel.get_busy():
            Player_audio.event_channel.stop()

        if able:
            Player_audio.event_channel.play(random.choice(Player_audio.opening_a_barrel_sounds))
        else:
            Player_audio.event_channel.play(Player_audio.cant_open_a_barrel_sound)

    def eating_audio(self) -> None:
        if Player_audio.event_channel.get_busy():
            Player_audio.event_channel.stop()
        Player_audio.event_channel.play(Player_audio.eating_sound)

    def drinking_audio(self) -> None:
        if Player_audio.event_channel.get_busy():
            Player_audio.event_channel.stop()
        Player_audio.event_channel.play(Player_audio.drinking_sound)

    def ghost_hurt_audio(self) -> None:
        if Player_audio.event_channel.get_busy():
            Player_audio.event_channel.stop()
        Player_audio.event_channel.play(Player_audio.ghost_hurt)


    def ghost_died_audio(self) -> None:
        if Player_audio.event_channel.get_busy():
            Player_audio.event_channel.stop()
        Player_audio.event_channel.play(Player_audio.ghost_died)
    def player_audio_update(self) -> None:
        Player_audio.player_movement_audio(self)
        Player_audio.player_hurt_audio(self)
        Player_audio.player_death_audio(self)


class Tile_Sounds:
    pygame.mixer.init()

    insert_key_sound = pygame.mixer.Sound(resource_path('audio/Tile_Sounds/Key_To_Slot.mp3'))
    pop_key_sound = pygame.mixer.Sound(resource_path('audio/Tile_Sounds/Key_From_Slot.mp3'))
    portal_open_sound = pygame.mixer.Sound(resource_path('audio/Tile_Sounds/Portal_Open_Sound.mp3'))
    portal_close_sound = pygame.mixer.Sound(resource_path('audio/Tile_Sounds/Portal_Close_Sound.mp3'))

    key_channel = pygame.mixer.Channel(6)
    portal_channel = pygame.mixer.Channel(7)

    audio_list = [insert_key_sound, pop_key_sound, portal_open_sound, portal_close_sound]

    for audio_name in audio_list:
        audio_name.set_volume(0.0)
        audio_name.play()
        audio_name.stop()

        # Muudab kogu mängu audio ära vastavalt sound_volume'ile
        audio_name.set_volume(UniversalVariables.sound_volume)

    def portal_open_audio(self) -> None:
        if Tile_Sounds.portal_channel.get_busy():
            Tile_Sounds.portal_channel.stop()

        Tile_Sounds.portal_channel.play(Tile_Sounds.portal_open_sound)

    def portal_close_audio(self) -> None:
        if Tile_Sounds.portal_channel.get_busy():
            Tile_Sounds.portal_channel.stop()

        Tile_Sounds.portal_channel.play(Tile_Sounds.portal_close_sound)

    def insert_key_audio(self) -> None:
        if Tile_Sounds.key_channel.get_busy():
            Tile_Sounds.key_channel.stop()

        Tile_Sounds.key_channel.play(Tile_Sounds.insert_key_sound)

    def pop_key_audio(self) -> None:
        if Tile_Sounds.key_channel.get_busy():
            Tile_Sounds.key_channel.stop()

        Tile_Sounds.key_channel.play(Tile_Sounds.pop_key_sound)
