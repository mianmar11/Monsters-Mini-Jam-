import pygame
from pygame.math import Vector2 as vec2

from scripts.entities.entity import Entity

class Player(Entity):
    def __init__(self, tile_size, pos):
        super().__init__(tile_size, pos)

        self.directions = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        self.speed = 2.4
    
    def move(self, tiles):
        self.y += self.vel.y * self.dt
        self.rect.y = self.y
        self.vertical_collision(tiles)
        self.rect.y = self.y

        self.x += self.vel.x * self.dt
        self.rect.x = self.x
        self.horizontal_collision(tiles)
        self.rect.x = self.x

    def keydown(self, key):
        if key == pygame.K_w:
            self.directions['up'] = True
        elif key == pygame.K_s:
            self.directions['down'] = True

        if key == pygame.K_d:
            self.directions['right'] = True
        elif key == pygame.K_a:
            self.directions['left'] = True
    
    def keyup(self, key):
        if key == pygame.K_w:
            self.directions['up'] = False
        elif key == pygame.K_s:
            self.directions['down'] = False

        if key == pygame.K_d:
            self.directions['right'] = False
        elif key == pygame.K_a:
            self.directions['left'] = False

    def set_vel(self):
        self.vel = vec2(0, 0)
        if self.directions['up']:
            self.vel.y = -1
        elif self.directions['down']:
            self.vel.y = 1
        
        if self.directions['right']:
            self.vel.x = 1
        elif self.directions['left']:
            self.vel.x = -1
        
        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * self.speed
    
    def update(self, delta_time):
        super().update(delta_time)

        self.set_vel()
    