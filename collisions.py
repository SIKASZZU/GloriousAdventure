import pygame

def check_collisions(self):
    keys = pygame.key.get_pressed()

    for hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id,\
            hit_box_offset_x, hit_box_offset_y in self.hit_boxes:

        # Saame olemasoleva blocki TOP-LEFT koordinaadid
        terrain_x = hit_box_x - hit_box_offset_x
        terrain_y = hit_box_y - hit_box_offset_y

        # See mis listis on, seda on vaja, et see listist ära võtta, ära võttes kaob see mapi pealt ära
        obj_hit_box = (hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id,
                        hit_box_offset_x, hit_box_offset_y)

        if object_id == 2:
            block_size = self.block_size

        if object_id == 4:
            block_size = self.block_size * 2
            terrain_x = terrain_x - self.block_size / 2
            terrain_y = terrain_y - self.block_size

        collision_terrain_rect = (terrain_x, terrain_y, block_size , block_size)
        if self.player_rect.colliderect(collision_terrain_rect):
            print("True")
            if keys[pygame.K_SPACE]:
                self.remove_object_at_position(hit_box_x, hit_box_y,
                                                terrain_x, terrain_y,
                                                obj_hit_box, object_id)

    on_land = False
    for i in range(len(self.terrain_data)):
        for j in range(len(self.terrain_data[i])):
            terrain_rect = pygame.Rect(
                j * self.block_size,
                i * self.block_size,
                self.block_size,
                self.block_size
            )

            # Vaatab kas player hitib midai v mitte
            if self.player_rect.colliderect(terrain_rect):
                in_water = any(
                    self.terrain_data[row][col] == 0
                    for row in range(i, i - 1, -1)
                    for col in range(j, j - 1, -1)
                )

                if in_water:
                    if keys[pygame.K_LSHIFT]:

                        # stamina = 0 - playeri speed = base speed
                        if self.player.stamina.current_stamina == 0:
                            self.player.stamina.stamina_regenerate(0.05)
                            self.player.speed = self.base_speed / 2

                        else:
                            self.player.speed = self.base_speed
                            self.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                            self.player.stamina.use_stamina(0.05)

                    else:
                        self.player.speed = self.base_speed / 2
                        self.player.stamina.stamina_regenerate(0.05)

                else:
                    on_land = True

    if on_land:
        if keys[pygame.K_LSHIFT]:
            # stamina = 0 - playeri speed = base speed
            if self.player.stamina.current_stamina == 0:
                self.player.stamina.stamina_regenerate(0.05)
                self.player.speed = self.base_speed
            else:
                self.player.speed = self.base_speed * 2.5
                self.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                self.player.stamina.use_stamina(0.05)

        else:
            self.player.speed = self.base_speed
            self.player.stamina.stamina_regenerate(0.05)