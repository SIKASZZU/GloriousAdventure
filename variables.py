import random

class UniversalVariables:
    player_x: int = random.randint(400, 400)
    player_y: int = random.randint(400, 400)
    
    block_size: int = 100
    player_height = block_size * 0.65
    player_width = block_size * 0.45