import pygame, math, random
from pygame.math import Vector2 as vec2

from scripts.utils import get_offset

class Bullet:
    def __init__(self, tile_size, pos, angle):
        self.tile_size = tile_size
        self.angle = angle

        self.hitbox = [self.tile_size/4, self.tile_size/4, self.tile_size/2, self.tile_size/2]

        self.image = pygame.Surface((self.tile_size, self.tile_size/2), pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(self.image, 'yellow', (0, 0, self.tile_size, self.tile_size/2))
        pygame.draw.rect(self.image, 'white', (1, 1, self.tile_size - 2, self.tile_size/2 - 2))

        self.x, self.y = pos[0] + self.tile_size * math.cos(math.radians(self.angle)), pos[1] + self.tile_size * math.sin(math.radians(self.angle))
        self.rect = pygame.Rect((0, 0), (self.hitbox[2], self.hitbox[3]))
        self.rect.center = (self.x, self.y)

        self.vel = vec2(1, 0)
        self.vel = self.vel.rotate(self.angle)
        self.speed = 10

        self.flash = pygame.Surface((self.tile_size, self.tile_size)).convert_alpha()
        self.flash.fill('white')
        self.flash = pygame.transform.rotate(self.flash, random.randint(0, 45))
        self.flash_timer = 0.8

        self.destruction_timer = 1000

        self.damage = 1

    def draw(self, draw_surf, camera_offset):
        if self.flash_timer > 0:
            img = self.flash
        else:
            img = self.image 
            img = pygame.transform.rotozoom(img, -self.angle, 1)
        render_x = self.rect.x - camera_offset[0] - (img.get_width() - self.hitbox[2]) / 2
        render_y = self.rect.y - camera_offset[1] - (img.get_height() - self.hitbox[3]) / 2
        
        draw_surf.blit(img, (render_x, render_y))
        # pygame.draw.polygon(draw_surf, 'red', [(self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]), (self.rect.x - camera_offset[0] + self.hitbox[2], self.rect.y - camera_offset[1]), (self.rect.x - camera_offset[0] + self.hitbox[2], self.rect.y - camera_offset[1] + self.hitbox[3]), (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1] + self.hitbox[3])], 1)
        # pygame.draw.rect(draw_surf, 'red', (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1], self.hitbox[2], self.hitbox[3]), 1)

    def collision(self, tile):
        if tile is None:
            return True
        if self.rect.colliderect(tile.rect) and tile.tile_type not in ('air', 'edge'):
            return True
        return False

    def destroy(self):
        self.destruction_timer -= self.dt
        if self.destruction_timer <= 0:
            return True
        return False

    def update(self, delta_time):
        self.dt = delta_time

        self.x += self.vel.x * self.speed * self.dt
        self.y += self.vel.y * self.speed * self.dt

        self.rect.centerx = self.x
        self.rect.centery = self.y

        self.flash_timer -= self.dt


class BulletManager:
    def __init__(self, tile_size):
        self.tile_size = tile_size

        self.bullets = []

    def add_bullet(self, pos, angle):
        self.bullets.append(Bullet(self.tile_size, pos, angle))
    
    def draw(self, draw_surf, camera_offset):
        for bullet in self.bullets:
            bullet.draw(draw_surf, camera_offset)

    def update(self, delta_time, tiles):
        self.dt = delta_time

        for bullet in self.bullets:
            bullet.update(self.dt)

            destroy = bullet.destroy()
            collided = bullet.collision(tiles.get(get_offset(bullet, self.tile_size), None))
            if destroy or collided:
                self.bullets.remove(bullet)