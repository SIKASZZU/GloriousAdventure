import random
from images import ground_images

# Koostab uue saare
def new_island(self, seed):
    self.generated_ground_images = {}

    # Seadistab juhuarvu genereerija seediga
    random.seed(seed)
    for x in range(self.X_max):
        for y in range(self.Y_max):
            # Leiab kauguse keskpunktist
            distance_to_center = ((x - self.center_x) ** 2 + (y - self.center_y) ** 2) ** 0.5
            normalized_distance = distance_to_center / self.max_distance
            land_probability = 1 - (normalized_distance ** 213)

            # Määrab pinnase maapinnaks, kui juhuslik arv on väiksem kui maapinna tõenäosus
            if random.random() < land_probability:
                self.terrain_data[x][y] = 1

                # Määrab juhusliku pinnase pildi genereeritud maapinnatüübile
                if not self.generated_ground_images.get((x, y)):
                    ground_image_name = f"Ground_{random.randint(0, 19)}"
                    ground_image = ground_images.get(ground_image_name)
                    self.generated_ground_images[(x, y)] = ground_image

    # Genereerib kivid ja puud
    for i in range(len(self.terrain_data)):
        for j in range(len(self.terrain_data[i])):
            if self.terrain_data[i][j] == 1:
                # Kontrollib, kas lahter peaks olema kivi või puu
                if random.random() < 0.03:
                    self.terrain_data[i][j] = 2  # Kivi
                elif random.random() < 0.04:
                    self.terrain_data[i][j] = 4  # Puu
