import random


columns = 5
rows = 5


# teeb row ja column suuruse 2D matrixi green : 1 (terraini)
terrain_data = {(row, column): {'color': 'green'} for row in range(rows) for column in range(columns)}


# Muudab random green (terrain) ruudu blueks (wateriks)
for _ in range(5):  
    random_row = random.randint(0, rows - 1)
    random_column = random.randint(0, columns - 1)
    terrain_data[(random_row, random_column)] = {'color': 'blue'}


# Kui on tekkinud 1 blue (water) ruut, ss yritab selle ymber juurde tekitada
def change_terrain_to_water(terrain_change_tile):
    try:
      if random.random() < 0.8:
          terrain_data[(random_row - 1, random_column - 1)] = {'color': 'blue'}
          print(f'Changed {terrain_data[(random_row - 1, random_column - 1)]} to blue: 2')
          print()
    except KeyError:
        print('Keyerror in function change_terrain_to_water')   


# Kui on tekkinud 1 blue (water) ruut, ss yritab selle ymber juurde tekitada
for _ in range(len(terrain_data)):
    if terrain_data[(random_row, random_column)] == {'color': 'blue'}:
      print(f'Found blue {terrain_data[(random_row, random_column)]}')

      try:  # Proovib muuta terraini VASAKUL
        tile = terrain_data[(random_row, random_column - 1)]
        if tile == {'color': 'blue'}:
            pass  #  K6rval (vasakul) ruut on juba sinine
        else:
          change_terrain_to_water(tile)
      except KeyError:
        print('Keyerror #1')

      try:  # Proovib muuta terraini PAREMAL
        tile = terrain_data[(random_row, random_column + 1)]
        if tile == {'color': 'blue'}:
            pass  #  K6rval (paremal) ruut on juba sinine
        else:
          change_terrain_to_water(tile)     
      except KeyError:
        print('Keyerror #2')

      try:  # Proovib muuta terraini YLEVAL
        tile = terrain_data[(random_row - 1, random_column)]
        if tile == {'color': 'blue'}:
            pass  #  K6rval (yleval) ruut on juba sinine
        else:
          change_terrain_to_water(tile)

      except KeyError:
        print('Keyerror #3')

      try:  # Proovib muuta terraini ALL
        tile = terrain_data[(random_row + 1, random_column)]
        if tile == {'color': 'blue'}:
            pass  #  K6rval (all) ruut on juba sinine
        else:
          change_terrain_to_water(tile)
      except KeyError:
        print('Keyerror #4')


# pohhuj printimine terminali
for row in range(rows):
    for column in range(columns):
        print(terrain_data[(row, column)], end='\t')
    print()
