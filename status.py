from variables import UniversalVariables


class PlayerEffect:
    def __init__(self, player):
        self.player = player
            
        # Poison
        self.poison_timer: int = 0
        self.poison_damage: float = 1
        self.poison_timer_list: list[int, ...] = [number for number in range(0, 1000 + 1, 200)]  # [0, 200, 400, 600, 800, 1000]

        # Bleed
        self.bleed_timer: int = 0
        self.bleed_damage: float = 1
        self.bleed_timer_list: list[int, ...] = [number for number in range(0, 1400 + 1, 200)]  # [0, 200, 400, 600, 800, 1000, 1200, 1400]

        # Todo: Infection
        # Placeholder

        # Cure
        self.cure_timer: int = 0
        self.cure_duration: int = 1000

    def update(self):
        PlayerEffect.bleed(self)
        PlayerEffect.poison(self)
        PlayerEffect.infection(self)
        PlayerEffect.cure(self)

    def poison(self):
        if not UniversalVariables.player_poisoned:
            return

        if self.poison_timer in self.poison_timer_list:
            self.player.health.damage(self.poison_damage)

        if self.poison_timer == self.poison_timer_list[-1]:
            UniversalVariables.player_poisoned = False
            self.poison_timer = 0

        self.poison_timer += 1

    def bleed(self, just_update=False):
        if not UniversalVariables.player_bleeding:
            return

        if self.bleed_timer in self.bleed_timer_list:
            self.player.health.damage(self.bleed_damage)

        if self.bleed_timer == self.bleed_timer_list[-1]:
            UniversalVariables.player_bleeding = False
            self.bleed_timer = 0

        self.bleed_timer += 1

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

        if self.cure_timer == 0:
            self.cure_timer = self.cure_duration

        if UniversalVariables.debug_mode:
            print('debug mode print: remaining_time', self.cure_timer, 'sec')

        if self.cure_timer > 0:
            self.cure_timer -= 1

        if self.cure_timer == 0:
            UniversalVariables.player_infected = False
            UniversalVariables.player_poisoned = False
            UniversalVariables.serum_active = False
            self.cure_timer = 0  # Reset the timer for future use