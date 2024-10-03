import random
import time

from variables import UniversalVariables


class PlayerStatus:
    # Poison
    poison_timer: int = 0
    poison_damage: float = 1
    poison_timer_list: list[int, ...] = [number for number in range(0, 1000 + 1, 200)]  # [0, 200, 400, 600, 800, 1000]

    # Bleed
    bleed_timer: int = 0
    bleed_damage: float = 1
    bleed_timer_list: list[int, ...] = [number for number in range(0, 1400 + 1, 200)]  # [0, 200, 400, 600, 800, 1000, 1200, 1400]

    # Todo: Infection
    # Placeholder

    # Cure
    cure_timer: int = 0
    cure_duration: int = 1000

    def update(self):
        PlayerStatus.bleed(self)
        PlayerStatus.poison(self)
        PlayerStatus.infection(self)
        PlayerStatus.cure(self)

    def poison(self):
        if not UniversalVariables.player_poisoned:
            return

        if PlayerStatus.poison_timer in PlayerStatus.poison_timer_list:
            self.player.health.damage(PlayerStatus.poison_damage)

        if PlayerStatus.poison_timer == PlayerStatus.poison_timer_list[-1]:
            UniversalVariables.player_poisoned = False
            PlayerStatus.poison_timer = 0

        PlayerStatus.poison_timer += 1

    def bleed(self, just_update=False):
        if not UniversalVariables.player_bleeding:
            return

        if PlayerStatus.bleed_timer in PlayerStatus.bleed_timer_list:
            self.player.health.damage(PlayerStatus.bleed_damage)

        if PlayerStatus.bleed_timer == PlayerStatus.bleed_timer_list[-1]:
            UniversalVariables.player_bleeding = False
            PlayerStatus.bleed_timer = 0

        PlayerStatus.bleed_timer += 1

        # + speed decreased when running // broken. vees on ikka sama kiire

    def infection(self):
        pass
        # + use more stamina
        # + more decreased hunger, resistence

        # increase water needence
        # hallucinations? -- fuck up the vision code :D

    def cure(self):
        if not UniversalVariables.serum_active:
            return

        # Kui effecte pole ss returnib
        if not UniversalVariables.player_infected and not UniversalVariables.player_poisoned:
            UniversalVariables.serum_active = False
            return

        if PlayerStatus.cure_timer == 0:
            PlayerStatus.cure_timer = PlayerStatus.cure_duration

        if UniversalVariables.debug_mode:
            print('debug mode print: remaining_time', PlayerStatus.cure_timer, 'sec')

        if PlayerStatus.cure_timer > 0:
            PlayerStatus.cure_timer -= 1

        if PlayerStatus.cure_timer == 0:
            UniversalVariables.player_infected = False
            UniversalVariables.player_poisoned = False
            UniversalVariables.serum_active = False
            PlayerStatus.cure_timer = 0  # Reset the timer for future use