import pygame


class Player_audio:

    # Initialize pygame
    pygame.mixer.init()

    player_hit_sound = pygame.mixer.Sound('audio/Player_Sounds/Player_Got_Hurt.wav')
    player_death = pygame.mixer.Sound('audio/Player_Sounds/Player_Died.wav')
    death_counter = 0
    current_health: int = None

    def __init__(self):
        self.player = None

    def player_movement_audio(self) -> None:
         pass

    def player_hurt_audio(self) -> None:
        # Kui current health puudub siis muudab selle playeri eludeks, mis tal hetkel oli
        if Player_audio.current_health is None:
            Player_audio.current_health = self.player.health.get_health()

        # Kui playeri kaotab elusi siis käid 'Player_hit' heli
        if Player_audio.current_health != self.player.health.get_health() and self.player.health.get_health() > 0:
            Player_audio.player_hit_sound.play()
            Player_audio.current_health = self.player.health.get_health()

        else:
            return

    def player_death_audio(self) -> None:
        if self.player.health.get_health() <= 0 and Player_audio.death_counter == 0:
            Player_audio.player_death.play()
            Player_audio.death_counter += 1

        else:
            return

    def player_audio_update(self) -> None:
        Player_audio.player_movement_audio(self)
        Player_audio.player_hurt_audio(self)
        Player_audio.player_death_audio(self)
