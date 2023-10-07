import pygame
from objects import Object_Management

class Collisions:

    def check_collisions(self) -> None:
        keys = pygame.key.get_pressed()

        for hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y in self.hit_boxes:

            # See mis listis on, seda on vaja, et see listist ära võtta, ära võttes kaob see mapi pealt ära
            obj_hit_box = (hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y)

            block_size: int = self.block_size
            #print('collisions', hit_box_x, hit_box_offset_x)
            terrain_x: int = hit_box_x - hit_box_offset_x
            terrain_y: int = hit_box_y - hit_box_offset_y

            if object_id == 4: block_size: int = self.block_size * 2  # object 4jal on teised m66tmed
            collision_object_rect = pygame.Rect(terrain_x, terrain_y, block_size , block_size)


            if self.player_rect.colliderect(collision_object_rect):
                if keys[pygame.K_SPACE] and self.can_pickup:
                    self.pickup_timer = pygame.time.get_ticks()
                    self.can_pickup = False  # Keelab j2rgmise pickupi

                # Check if the pickup delay has passed
                current_time = pygame.time.get_ticks()
                if not self.can_pickup and current_time - self.pickup_timer >= self.pickup_delay * 1000:  # Convert seconds to milliseconds
                    self.can_pickup = True  # Lubaks j2rgmise pickupi

                    Object_Management.remove_object_at_position(self, terrain_x, terrain_y, object_id)
                    Object_Management.add_object_to_inv(self, object_id, obj_hit_box)
                else: pass


                # Vajalik, et teada kas player renderida peale v6i enne objekte
                # Y-v22rtus == object_rectil [1] /// Y + 60, sest ss on v2he normaalsem see puutagant v2ljatulek
                if (collision_object_rect[1] + 60) <= self.player_rect[1]: self.render_after = True
                else:  self.render_after = False

        Collisions.collision_hitbox(self)

    ### BROKEN

    # sest see vaatab ainult x ja y top cordinaati ja ta ei kontrolli teisi nurki ehk siis sama asi mis oli selle vee pasaga

    def collision_hitbox(self):
            for hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y in self.hit_boxes:
                collision_object_hitbox = pygame.Rect(hit_box_x, hit_box_y, hit_box_width, hit_box_height)

                # Calculate the player's corner positions
                top_left_player_x = self.player_x
                top_left_player_y = self.player_y
                top_right_player_x = self.player_x + self.player_width
                top_right_player_y = self.player_y
                bottom_left_player_x = self.player_x
                bottom_left_player_y = self.player_y + self.player_height
                bottom_right_player_x = self.player_x + self.player_width
                bottom_right_player_y = self.player_y + self.player_height

                # Check for collision using all four corners of the player character
                top_left_collision = collision_object_hitbox.collidepoint(top_left_player_x, top_left_player_y)
                top_right_collision = collision_object_hitbox.collidepoint(top_right_player_x, top_right_player_y)
                bottom_left_collision = collision_object_hitbox.collidepoint(bottom_left_player_x, bottom_left_player_y)
                bottom_right_collision = collision_object_hitbox.collidepoint(bottom_right_player_x, bottom_right_player_y)

                # Check for collisions on the right side
                if top_right_collision or bottom_right_collision:
                    if self.player_x < hit_box_x:
                        self.player_x -= 4

                # Check for collisions on the left side
                if top_left_collision or bottom_left_collision:
                    if self.player_x + self.player_width > (hit_box_x + hit_box_width):
                        self.player_x += 4

                # Check for collisions from bottom to top
                if bottom_left_collision or bottom_right_collision:
                    if self.player_y < hit_box_y:
                        self.player_y -= 4

                # Check for collisions from top to bottom
                if top_left_collision or top_right_collision:
                    if self.player_y + self.player_height > (hit_box_y + hit_box_height):
                        self.player_y += 4

                # Additional collision handling code can be added as needed


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


