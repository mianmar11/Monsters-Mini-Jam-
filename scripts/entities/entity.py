import pygame    
from pygame.math import Vector2 as vec2

class Entity:
    def __init__(self, tile_size, pos):
        self.tile_size = tile_size
        self.x, self.y = pos[0] * self.tile_size, pos[1] * self.tile_size

        self.image = pygame.Surface((self.tile_size, self.tile_size)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.image.fill('blue')

        self.vel = vec2(0, 0)
        self.ext_vel = vec2(0, 0)

    def draw(self, draw_surf, camera_offset):
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]

        draw_surf.blit(self.image, (render_x, render_y))
    
    def move(self, tiles):
        if self.vel.length() > 0:
            self.vel = self.vel.normalize()

        self.y += (self.vel.y * self.speed + self.ext_vel.y) * self.dt
        self.rect.y = self.y
        self.vertical_collision(tiles)
        self.rect.y = self.y

        self.x += (self.vel.x * self.speed + self.ext_vel.x) * self.dt
        self.rect.x = self.x
        self.horizontal_collision(tiles)
        self.rect.x = self.x

    def vertical_collision(self, tiles):
        for tile in tiles:

            if tile.rect.colliderect(self.rect):
                # # single process
                # if self.ext_vel.y < 0:
                #     self.y = tile.rect.bottom
                #     self.ext_vel.y = 0
                
                # elif self.ext_vel.y > 0:
                #     self.y = tile.rect.top - self.rect.h
                #     self.ext_vel.y = 0

                # if self.vel.y < 0:
                #     self.y = tile.rect.bottom
                #     self.vel.y = 0
                
                # elif self.vel.y > 0:
                #     self.y = tile.rect.top - self.rect.h
                #     self.vel.y = 0
                
                # dual process
                if self.vel.y < 0 and self.ext_vel.y > 0:
                    self.y = tile.rect.bottom
                    self.vel.y = 0
                    self.ext_vel.y = 0
                
                elif self.vel.y > 0 and self.ext_vel.y < 0:
                    self.y = tile.rect.top - self.rect.h
                    self.vel.y = 0
                    self.ext_vel.y = 0

                elif self.vel.y > 0 and self.ext_vel.y > 0:
                    self.y = tile.rect.top - self.rect.h
                    self.vel.y = 0
                    self.ext_vel.y = 0
                
                elif self.vel.y < 0 and self.ext_vel.y < 0:
                    self.y = tile.rect.bottom
                    self.vel.y = 0
                    self.ext_vel.y = 0


                elif self.vel.y == 0 and self.ext_vel.y > 0:
                    self.y = tile.rect.top - self.rect.h
                    self.ext_vel.y = 0
                
                elif self.vel.y == 0 and self.ext_vel.y < 0:
                    self.y = tile.rect.bottom
                    self.ext_vel.y = 0

                elif self.vel.y < 0 and self.ext_vel.y == 0:
                    self.y = tile.rect.bottom
                    self.vel.y = 0
                
                elif self.vel.y > 0 and self.ext_vel.y == 0:
                    self.y = tile.rect.top - self.rect.h
                    self.vel.y = 0

    def horizontal_collision(self, tiles):
        for tile in tiles:

            if tile.rect.colliderect(self.rect):
                # # single process
                # if self.ext_vel.x < 0:
                #     self.x = tile.rect.right
                #     self.ext_vel.x = 0
                
                # elif self.ext_vel.x > 0:
                #     self.x = tile.rect.left - self.rect.w
                #     self.ext_vel.x = 0
                
                # elif self.vel.x < 0:
                #     self.x = tile.rect.right
                #     self.vel.x = 0
                
                # elif self.vel.x > 0:
                #     self.x = tile.rect.left - self.rect.w
                #     self.vel.x = 0
                
                # dual process
                if self.vel.x < 0 and self.ext_vel.x > 0:
                    self.x = tile.rect.right
                    self.vel.x = 0
                    self.ext_vel.x = 0
                
                elif self.vel.x > 0 and self.ext_vel.x < 0:
                    self.x = tile.rect.left - self.rect.w
                    self.vel.x = 0
                    self.ext_vel.x = 0
                
                elif self.vel.x > 0 and self.ext_vel.x > 0:
                    self.x = tile.rect.left - self.rect.w
                    self.vel.x = 0
                    self.ext_vel.x = 0
                
                elif self.vel.x < 0 and self.ext_vel.x < 0:
                    self.x = tile.rect.right
                    self.vel.x = 0
                    self.ext_vel.x = 0
                    

                elif self.vel.x == 0 and self.ext_vel.x > 0:
                    self.x = tile.rect.left - self.rect.w
                    self.ext_vel.x = 0
                
                elif self.vel.x == 0 and self.ext_vel.x < 0:
                    self.x = tile.rect.right
                    self.ext_vel.x = 0
                
                elif self.vel.x < 0 and self.ext_vel.x == 0:
                    self.x = tile.rect.right
                    self.vel.x = 0
                
                elif self.vel.x > 0 and self.ext_vel.x == 0:
                    self.x = tile.rect.left - self.rect.w
                    self.vel.x = 0
                
    def update(self, delta_time):
        self.dt = delta_time

        if round(self.ext_vel.length(), 2) < 0.1:
            self.ext_vel = vec2(0, 0)
        else:
            self.ext_vel.x += (0 - self.ext_vel.x) * self.dt
            self.ext_vel.y += (0 - self.ext_vel.y) * self.dt
        