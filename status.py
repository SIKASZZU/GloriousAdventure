import random
import time

from variables import UniversalVariables


class PlayerStatus:
    bleed_damage_timer = 0
    times_of_bleed     = 0
    bleed_damage       = 0.25
    cure_timer         = 0
    cure_start_time    = None

    def update(self):
        PlayerStatus.bleed(self, just_update=True)
        PlayerStatus.infection(self, just_update=True)
        PlayerStatus.cure()

    def bleed(self, just_update=False):
        if UniversalVariables.player_bleeding == False and just_update == False:  # see justupdate kontrollib, et see munk lambist niisama seda bleedi playerile ei spawni
            random_number = random.randint(1, 10)
            if random_number <= 6:            
                UniversalVariables.player_bleeding = True

        if UniversalVariables.player_bleeding == True:
            PlayerStatus.bleed_damage_timer += 1

            if PlayerStatus.bleed_damage_timer >= 100:
                self.player.health.damage(PlayerStatus.bleed_damage)
                PlayerStatus.bleed_damage_timer = 0
                PlayerStatus.times_of_bleed += 1

                if PlayerStatus.times_of_bleed == 15:
                    PlayerStatus.times_of_bleed = 0
                    UniversalVariables.player_bleeding = False

        # + speed decreased when running // broken . vees on ikka sama kiire

    ### TODO: 2kki infection peaks olema kohe bleedi all.
    def infection(self, just_update=False):
        if UniversalVariables.player_infected == False and just_update == False:
            random_number = random.randint(1, 10)
            if random_number <= 3:
                UniversalVariables.player_infected = True

            # + use more stamina
            # + more decreased hunger, resistence
            
            # increase water needence
            # hallucinations? -- fuck up the vision code :D
    
    def cure():
        
        if UniversalVariables.serum_active == True:  
            ### TODO: funktsioon, mis readib sekundied (time.perf_counter)
            if PlayerStatus.cure_start_time is None:
                PlayerStatus.cure_start_time = time.perf_counter()

            elapsed_time = time.perf_counter() - PlayerStatus.cure_start_time
            remaining_time = 15 - int(elapsed_time)
        
            if UniversalVariables.debug_mode == True:  print('debug mode print: remaining_time', remaining_time, 'sec')
            if remaining_time <= 0:
                PlayerStatus.cure_start_time = None
                UniversalVariables.player_infected = False
                UniversalVariables.serum_active = False
                


