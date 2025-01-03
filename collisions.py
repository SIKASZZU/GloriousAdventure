import pygame



class Collisions:

    def __init__(self, player, player_update, terrain_data, hud, render, variables, COLLISION_ITEMS):
        self.player = player
        self.player_update = player_update
        self.terrain_data = terrain_data
        self.hud = hud
        self.render = render
        self.variables = variables
        self.COLLISION_ITEMS = COLLISION_ITEMS

    # FIXME: terve player collision wallide ja asjadega tuleb ära fixida
        # see voiks olla smoothim.
    def player_hit_collision(self, collision_box) -> None:
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte

        # Kui player jookseb siis ta ei lähe läbi objektide
        if keys[pygame.K_LSHIFT] and self.player.stamina.current_stamina != 0:
            collision_move = 10
        else:
            collision_move = 4

        # Arvutab, kui palju objekti hitbox on suurem (või väiksem) kui mängija hitbox
        dx = (self.player_update.player_rect.centerx - collision_box.centerx) / (self.variables.player_width / 2 + collision_box[2] / 2)
        dy = (self.player_update.player_rect.centery - collision_box.centery) / (self.variables.player_height / 2 + collision_box[3] / 2)

        if abs(dx) > abs(dy):
            if dx > 0:  self.variables.player_x += collision_move  # Liigutab mängijat paremale
            else:  self.variables.player_x -= collision_move  # Liigutab mängijat vasakule

        else:
            if dy > 0:  self.variables.player_y += collision_move  # Liigutab mängijat alla
            else:  self.variables.player_y -= collision_move  # Liigutab mängijat ülesse


    def collison_terrain_types(self) -> None:
        keys = pygame.key.get_pressed()

        sprinting = keys[pygame.K_LSHIFT] and keys[pygame.K_d] or \
                    keys[pygame.K_LSHIFT] and keys[pygame.K_a] or \
                    keys[pygame.K_LSHIFT] and keys[pygame.K_w] or \
                    keys[pygame.K_LSHIFT] and keys[pygame.K_s]

        sneaking = keys[pygame.K_LCTRL] and keys[pygame.K_d] or \
                    keys[pygame.K_LCTRL] and keys[pygame.K_a] or \
                    keys[pygame.K_LCTRL] and keys[pygame.K_w] or \
                    keys[pygame.K_LCTRL] and keys[pygame.K_s]

        walking = keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]

        player_grid_row = int(self.variables.player_x // self.variables.block_size)
        player_grid_col = int(self.variables.player_y // self.variables.block_size)

        # Siin peavad need for loopid olema, sest muidu tekib mingisugune offset tiks ja for loopid sunnivad asju windowi j2rgi tegema.
        for row in range(player_grid_col - self.render.render_range, player_grid_col + self.render.render_range + 1):
            for col in range(player_grid_row - self.render.render_range, player_grid_row + self.render.render_range + 1):

                terrain_rect = pygame.Rect(col * self.variables.block_size, row * self.variables.block_size,
                                           self.variables.block_size, self.variables.block_size)

                # see asi somehow ei lase staminal instantly tyhjaks joosta? Kas player ei ole mitte kogu eag terrainrectiga collisionis??
                if not self.player_update.player_rect.colliderect(terrain_rect):
                    continue

                try:
                    if self.terrain_data[row][col] in self.COLLISION_ITEMS.value:
                        self.player_hit_collision(terrain_rect)

                    else:
                        #player statei loomine
                        self.variables.player_sprinting = False
                        self.variables.player_sneaking  = False
                        self.variables.player_walking   = False
                        self.variables.player_standing  = False

                        if sprinting:
                            self.variables.player_sprinting = True

                        elif sneaking:
                            self.variables.player_sneaking  = True
                        
                        elif walking:
                            self.variables.player_walking  = True
                        
                        else:
                            self.variables.player_standing = True

                        if 0 <= row < len(self.terrain_data) and 0 <= col < len(self.terrain_data[row]):
                            in_water = self.terrain_data[row][col] == 0

                            # kui player on haige, infected, ss selle jaoks k2rbib teatud v22rtusi
                            stamina_cost = 0.05
                            stamina_regen = 0.05
                            if self.variables.player_infected == True:
                                stamina_cost = 0.15
                                stamina_regen = 0.025

                            run_speed_multiplier = 1.5
                            if self.variables.player_bleeding == True:
                                run_speed_multiplier = 1.2

                            if in_water == False:
                                if sprinting:  # Player asub maal
                                    # stamina = 0 - playeri speed = base speed
                                    if self.player.stamina.current_stamina == 0:
                                        self.player.stamina.stamina_regenerate(stamina_regen)
                                        self.player.speed.current_speed = self.player.speed.base_speed
                                        self.variables.player_sprinting = False  # stamina on otsas // et ei displayiks high volumeit

                                    else:
                                        self.player.speed.current_speed = self.player.speed.base_speed * run_speed_multiplier
                                        self.hud.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                                        self.player.stamina.use_stamina(stamina_cost)

                                elif sneaking:
                                    self.player.speed.current_speed = self.player.speed.base_speed // 2
                                    self.player.stamina.stamina_regenerate(stamina_regen)

                                else:  # tavaline kondimine
                                    self.player.speed.current_speed = self.player.speed.base_speed
                                    self.player.stamina.stamina_regenerate(stamina_regen)


                            else:  # Player asub vees
                                if sprinting:
                                    # stamina = 0 - playeri speed = base speed
                                    if self.player.stamina.current_stamina == 0:
                                        self.player.stamina.stamina_regenerate(stamina_regen)
                                        self.player.speed.current_speed = self.player.speed.base_speed / 2
                                        self.variables.player_sprinting = False  # stamina on otsas // et ei displayks high volumit

                                    else:
                                        self.player.speed.current_speed = self.player.speed.base_speed
                                        self.hud.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                                        self.player.stamina.use_stamina(stamina_cost)

                                else:
                                    self.player.speed.current_speed = self.player.speed.base_speed / 2
                                    self.player.stamina.stamina_regenerate(stamina_regen)

                except Exception as e:  print('Error @ collisions.py, collison_terrain_types:', e)