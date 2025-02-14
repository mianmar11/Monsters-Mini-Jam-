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

    def draw(self, draw_surf, camera_offset):
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]

        draw_surf.blit(self.image, (render_x, render_y))
    
    def vertical_collision(self, tiles):
        for tile in tiles:
            if not (tile.tile_type == 'air' or tile.tile_type == 'edge'):
                continue

            if tile.rect.colliderect(self.rect):
                if self.vel.y < 0:
                    self.y = tile.rect.bottom
                    self.vel.y = 0
                
                elif self.vel.y > 0:
                    self.y = tile.rect.top - self.rect.h
                    self.vel.y = 0

    def horizontal_collision(self, tiles):
        for tile in tiles:
            if not (tile.tile_type == 'air' or tile.tile_type == 'edge'):
                continue

            if tile.rect.colliderect(self.rect):
                if self.vel.x < 0:
                    self.x = tile.rect.right
                    self.vel.x = 0
                
                elif self.vel.x > 0:
                    self.x = tile.rect.left - self.rect.w
                    self.vel.x = 0

    def update(self, delta_time):
        self.dt = delta_time
        