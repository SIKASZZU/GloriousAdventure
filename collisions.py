import pygame
from items import items_list
from objects import Object_Management


class Collisions:

    def check_collisions(self) -> None:
        keys = pygame.key.get_pressed()

        # Object id, pilt, ja pildi suurus
        interaction_boxes = {}

        for hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y in self.hit_boxes:

            # See mis listis on, seda on vaja, et see listist ära võtta, ära võttes kaob see mapi pealt ära
            obj_hit_box = (
            hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y)

            block_size: int = self.block_size
            terrain_x: int = hit_box_x - hit_box_offset_x
            terrain_y: int = hit_box_y - hit_box_offset_y

            for item in items_list:
                if item.get("Type") == "Object" and item.get("ID") == object_id:
                    width = item.get("Object_width")
                    height = item.get("Object_height")

                    interaction_boxes[object_id] = (width, height)

            collision_object_rect = pygame.Rect(terrain_x, terrain_y, width, height)

            if self.player_rect.colliderect(collision_object_rect):
                print(obj_hit_box)

                if keys[pygame.K_SPACE] and self.can_pickup:

                    Object_Management.remove_object_at_position(self, terrain_x, terrain_y, object_id)
                    Object_Management.add_object_to_inv(self, object_id, obj_hit_box)

                if (collision_object_rect[1] + self.block_size * 1.2) <= self.player_rect[1]:
                    self.render_after = True
                else:
                    self.render_after = False

        Collisions.collision_hitbox(self)

    def collision_hitbox(self):
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte
        for \
                hit_box_x, hit_box_y, \
                hit_box_width, hit_box_height,\
                object_id, hit_box_offset_x,\
                hit_box_offset_y in self.hit_boxes:

            collision_object_hitbox = pygame.Rect(hit_box_x, hit_box_y, hit_box_width, hit_box_height)

            # Kui player jookseb siis ta ei lähe läbi objektide
            if keys[pygame.K_LSHIFT] and self.player.stamina.current_stamina != 0:
                collision_move = 10

            else:
                collision_move = 4

            # Kui läheb vastu hitboxi siis ei lase sellest läbi minna
            if self.player_rect.colliderect(collision_object_hitbox):

                # Arvutab, kui palju objekti hitbox on suurem (või väiksem) kui mängija hitbox
                dx = (self.player_rect.centerx - collision_object_hitbox.centerx) / (
                            self.player_width / 2 + hit_box_width / 2)
                dy = (self.player_rect.centery - collision_object_hitbox.centery) / (
                            self.player_height / 2 + hit_box_height / 2)

                # Horisontaalne kokkupuude
                if abs(dx) > abs(dy):
                    # Paremalt poolt
                    if dx > 0:
                        self.player_x += collision_move  # Liigutab mängijat paremale
                    # Vasakultpoolt
                    else:
                        self.player_x -= collision_move  # Liigutab mängijat vasakule

                # Vertikaalne kokkupuude
                else:
                    # Alt
                    if dy > 0:
                        self.player_y += collision_move  # Liigutab mängijat alla
                    # Ülevalt
                    else:
                        self.player_y -= collision_move  # Liigutab mängijat ülesse

    def collison_terrain(self) -> None:
        render_range: int = self.render_range
        keys = pygame.key.get_pressed()

        player_grid_row = int(self.player_x // self.block_size)
        player_grid_col = int(self.player_y // self.block_size)

        # Vaatab terraini mida ta renerib ja selle järgi kontrollib collisoneid
        for i in range(player_grid_col - render_range, player_grid_col + render_range + 1):
            for j in range(player_grid_row - render_range, player_grid_row + render_range + 1):

                # Vaatab terrain recti ja playeri collisoneid
                terrain_rect = pygame.Rect(j * self.block_size, i * self.block_size, self.block_size, self.block_size)
                if self.player_rect.colliderect(terrain_rect):

                    # Kontrollib kas terrain block jääb faili self.terrain_data piiridesse
                    if 0 <= i < len(self.terrain_data) and 0 <= j < len(self.terrain_data[i]):

                        in_water = self.terrain_data[i][j] == 0
                        if in_water != True:
                            # Player asub maal
                            if keys[pygame.K_LSHIFT]:
                                # stamina = 0 - playeri speed = base speed
                                if self.player.stamina.current_stamina == 0:
                                    self.player.stamina.stamina_regenerate(0.05)
                                    self.player.speed.current_speed = self.player.speed.base_speed
                                else:
                                    self.player.speed.current_speed = self.player.speed.base_speed * 2.5
                                    self.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                                    self.player.stamina.use_stamina(0.05)
                            else:
                                self.player.speed.current_speed = self.player.speed.base_speed
                                self.player.stamina.stamina_regenerate(0.05)

                        ### Siin on koodikordus sellest, et kas on vees v6i mapist v2ljas.

                        else:  # Player asub vees
                            if keys[pygame.K_LSHIFT]:
                                # stamina = 0 - playeri speed = base speed
                                if self.player.stamina.current_stamina == 0:
                                    self.player.stamina.stamina_regenerate(0.05)
                                    self.player.speed.current_speed = self.player.speed.base_speed / 2
                                else:
                                    self.player.speed.current_speed = self.player.speed.base_speed
                                    self.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                                    self.player.stamina.use_stamina(0.05)
                            else:
                                self.player.speed.current_speed = self.player.speed.base_speed / 2
                                self.player.stamina.stamina_regenerate(0.05)

                    else:  # Player asub mapist v2ljas
                        if keys[pygame.K_LSHIFT]:

                            # stamina = 0 - playeri speed = base speed
                            if self.player.stamina.current_stamina == 0:
                                self.player.stamina.stamina_regenerate(0.05)
                                self.player.speed.current_speed = self.player.speed.base_speed / 2
                            else:
                                self.player.speed.current_speed = self.player.speed.base_speed
                                self.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                                self.player.stamina.use_stamina(0.05)
                        else:
                            self.player.speed.current_speed = self.player.speed.base_speed / 2
                            self.player.stamina.stamina_regenerate(0.05)

