class Player:
    def __init__(self, name, health=100, stamina=100):
        self.name = name
        self.health = health
        self.stamina = stamina
        self.current_tile = 0  # Default tile
        
    def move_to_tile(self, tile_number):
        self.current_tile = tile_number
        if self.current_tile == 4:  # Tile with water
            self.swimming()

    def swimming(self):
        if self.stamina == 0:
            self.health -= 5
        else:
            self.stamina -= 10

        if self.health <= 0:
            print(f"{self.name} has died!")
