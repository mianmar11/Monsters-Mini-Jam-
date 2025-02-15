import pygame, math
from pygame.math import Vector2 as vec2

class Bullet:
    def __init__(self, tile_size, pos, angle):
        self.tile_size = tile_size

        self.hitbox = [0, 0, self.tile_size, self.tile_size/2]

        self.image = pygame.Surface((self.tile_size, self.tile_size/2), pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(self.image, 'yellow', self.hitbox)
        pygame.draw.rect(self.image, 'white', (1, 1, self.hitbox[2] - 2, self.hitbox[3] - 2))

        self.angle = angle
        self.x, self.y = self.hitbox[0] + pos[0] + self.tile_size * math.cos(math.radians(self.angle)), self.hitbox[1] + pos[1] + self.tile_size * math.sin(math.radians(self.angle))
        self.rect = pygame.Rect((0, 0), (self.hitbox[2], self.hitbox[3]))
        self.rect.center = (self.x, self.y)

        self.vel = vec2(1, 0)
        self.vel = self.vel.rotate(self.angle)
        self.speed = 10

    def draw(self, draw_surf, camera_offset):
        img = self.image
        img = pygame.transform.rotozoom(img, -self.angle, 1)
        render_x = self.rect.x - camera_offset[0] - self.hitbox[0] - (img.get_width() - self.image.get_width()) / 2
        render_y = self.rect.y - camera_offset[1] - self.hitbox[1] - (img.get_height() - self.image.get_height()) / 2
        
        draw_surf.blit(img, (render_x, render_y))
        # pygame.draw.rect(draw_surf, 'red', (self.rect.x - camera_offset[0] - (img.get_width() - self.image.get_width()) / 2, self.rect.y - camera_offset[1] - (img.get_height() - self.image.get_height()) / 2, self.hitbox[2], self.hitbox[3]), 1)

    def update(self, delta_time):
        self.dt = delta_time

        self.x += self.vel.x * self.speed * self.dt
        self.y += self.vel.y * self.speed * self.dt

        self.rect.centerx = self.x
        self.rect.centery = self.y


class BulletManager:
    def __init__(self, tile_size):
        self.tile_size = tile_size

        self.bullets = []

    def add_bullet(self, pos, angle):
        self.bullets.append(Bullet(self.tile_size, pos, angle))
    
    def draw(self, draw_surf, camera_offset):
        for bullet in self.bullets:
            bullet.draw(draw_surf, camera_offset)

    def update(self, delta_time):
        self.dt = delta_time

        for bullet in self.bullets:
            bullet.update(self.dt)
