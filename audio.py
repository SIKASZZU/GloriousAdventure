import pygame


class Player_audio:

    # Initialize pygame
    pygame.mixer.init()

    player_hit_sound = pygame.mixer.Sound('audio/player_hit.wav')
    player_death = pygame.mixer.Sound('audio/player_hit.wav')

    current_health: int = None

    def __init__(self):
        self.player = None

    def player_got_hurt(self):

        # Kui current health puudub siis muudab selle playeri eludeks, mis tal hetkel oli
        if Player_audio.current_health is None:
            Player_audio.current_health = self.player.health.get_health()

        # Kui playeri kaotab elusi siis käid 'Player_hit' heli
        if Player_audio.current_health != self.player.health.get_health():
            Player_audio.player_hit_sound.play()
            Player_audio.current_health = self.player.health.get_health()

        if self.player.health.get_health() <= 0:
            Player_audio.player_death.play()

        else:
            return

