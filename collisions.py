import pygame
import objects


def check_collisions(self) -> None:
    keys = pygame.key.get_pressed()

    for hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y in self.hit_boxes:

        # See mis listis on, seda on vaja, et see listist ära võtta, ära võttes kaob see mapi pealt ära
        obj_hit_box = (hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y)

        block_size: int = self.block_size
        terrain_x: int = hit_box_x - hit_box_offset_x
        terrain_y: int = hit_box_y - hit_box_offset_y

        try:
            if object_id == 4: 
                block_size: int = self.block_size * 2
            collision_object_rect = pygame.Rect(terrain_x, terrain_y, block_size , block_size)
        except TypeError:
            pass
        
        if self.player_rect.colliderect(collision_object_rect):
            if keys[pygame.K_SPACE]:

                # Et visuaalselt võtaks puu ära
                if object_id == 4:
                    terrain_x = terrain_x - self.block_size / 2
                    terrain_y = terrain_y - self.block_size

                objects.remove_object_at_position(self, terrain_x, terrain_y, object_id)  # removib itemi maailmast nahhuj
                objects.add_object_to_inv(self, object_id, obj_hit_box)
        
        
        if self.player_rect.colliderect(collision_object_rect):
            if (collision_object_rect[1] + 60) <= self.player_rect[1]:  # Y-v22rtus objectil [1], idk mdea kuidas teisiti seda saaks atm xD... +60 y value sest ss on v2he normaalsem see puutagant v2ljatulek
                self.render_after = True

            else: 
                self.render_after = False

### BROKEN

#        collision_object_hitbox = pygame.Rect(hit_box_x, hit_box_y, hit_box_width, hit_box_height)
#
#        if self.player_rect.colliderect(collision_object_hitbox):
#            print('collision')
#            if self.player_x < hit_box_x:
#                self.player_x -= 30
#            if self.player_x > (hit_box_x + hit_box_width):
#                self.player_x += 30
#
#            if self.player_y < hit_box_y:
#                self.player_y -= 30
#            if self.player_y > (hit_box_y + hit_box_height):
#                self.player_y += 30

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
                                self.player.speed = self.base_speed
                            else:
                                self.player.speed = self.base_speed * 2.5
                                self.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                                self.player.stamina.use_stamina(0.05)
                        else:
                            self.player.speed = self.base_speed
                            self.player.stamina.stamina_regenerate(0.05)

### Siin on koodikordus sellest, et kas on vees v6i mapist v2ljas.

                    else:  # Player asub vees v6i mapist v2ljas
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

                else:  # Player asub vees v6i mapist v2ljas
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
                    

