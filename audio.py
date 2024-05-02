import pygame
from variables import UniversalVariables


class Player_audio:
    # Initialize pygame
    pygame.mixer.init()

    previous_ground_sound = None

    player_hit_sound = pygame.mixer.Sound('audio/Player_Sounds/Player_Got_Hurt.wav')
    player_death_sound = pygame.mixer.Sound('audio/Player_Sounds/Player_Died.wav')

    maze_ground_sound = pygame.mixer.Sound('audio/Tile_Sounds/Maze_Ground_Sound.wav')
    water_sound = pygame.mixer.Sound('audio/Tile_Sounds/Water_Sound.mp3')

    # Preload'ib soundid groundi, puude, kivide, jne peal liikumiseks
    grass_sounds = [
        pygame.mixer.Sound('audio/Tile_Sounds/Grass_left_Foot_Sound.mp3'),
        pygame.mixer.Sound('audio/Tile_Sounds/Grass_Right_Foot_Sound.mp3'),
    ]
    current_grass_sound_index = 0

    grass_channel = pygame.mixer.Channel(1)  # Seob 1. channeli groundiga
    water_channel = pygame.mixer.Channel(2)  # Seob 2. channeli veega
    maze_channel = pygame.mixer.Channel(3)  # Seob 3. channeli maze'iga

    player_channel = pygame.mixer.Channel(5)  # Seob 5. channeli playeriga


    death_counter = 0
    current_health: int = None

    water_sound_list: list[int, ...] = [0]
    ground_sound_list: list[int, ...] = [1, 2, 4, 7, 107]
    maze_ground_list: list[int, ...] = [11, 89, 90, 91, 92, 93, 933, 94, 95, 96, 97, 977, 98, 988, 99]
    audio_list: list[str, ...] = [player_death_sound, player_hit_sound, grass_sounds, water_sound, maze_ground_sound]

    for audio_name in audio_list:
        if type(audio_name) == list:

            for grass_sound_name in grass_sounds:
                grass_sound_name.set_volume(0.0)
                grass_sound_name.play()
                grass_sound_name.stop()
                grass_sound_name.set_volume(UniversalVariables.sound_volume)

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

                        Player_audio.grass_channel.play(Player_audio.grass_sounds[Player_audio.current_grass_sound_index])
                        Player_audio.current_grass_sound_index = (Player_audio.current_grass_sound_index + 1) % len(Player_audio.grass_sounds)

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

    def player_audio_update(self) -> None:
        Player_audio.player_movement_audio(self)
        Player_audio.player_hurt_audio(self)
        Player_audio.player_death_audio(self)
