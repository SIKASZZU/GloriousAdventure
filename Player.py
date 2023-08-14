# Impordi nii:
# from player import user

class Player():
    def __init__(self, health, stamina, speed):
        self.health = health
        self.stamina = stamina
        self.speed = speed

user = Player(health=10, stamina=10, speed=4)
