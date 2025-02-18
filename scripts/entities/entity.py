import pygame    
from pygame.math import Vector2 as vec2

class Entity:
    def __init__(self, tile_size, pos):
        self.tile_size = tile_size
        self.x, self.y = pos[0] * self.tile_size, pos[1] * self.tile_size
        self.ori_pos = self.x, self.y

        self.image = pygame.Surface((self.tile_size, self.tile_size)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.image.fill('blue')

        self.shadow = pygame.Surface((self.tile_size + self.tile_size/4, self.tile_size/1.5)).convert_alpha()
        self.shadow.fill((0, 0, 0))
        self.shadow.set_alpha(48)
        
        self.scale_x = 1.0
        self.scale_y = 1.0

        self.vel = vec2(0, 0)
        self.ext_vel = vec2(0, 0)
        self.total_vel = vec2(0, 0)

        self.health = 5
        self.flicker_timer = 0
        self.damage_taken_cooldown = 15

        self.damage_timer = 0

    def deduct_health(self, damage=1):
        if self.damage_timer < 0:
            self.health -= damage
            self.damage_timer = self.damage_taken_cooldown
            self.flicker_timer = 24
            return True
        return
    
    def draw(self, draw_surf, camera_offset):
        scale_x = self.scale_x
        scale_y = self.scale_y

        img = pygame.transform.scale(self.image.copy(), (self.image.get_width() * scale_x, self.image.get_height() * scale_y))
        
        if self.flicker_timer > 0 and int(self.flicker_timer) % 6 == 0:
            img.fill('red')

        render_x = self.rect.x - camera_offset[0] - (img.get_width() - self.image.get_width()) / 2
        render_y = self.rect.y - camera_offset[1] - (img.get_width() - self.image.get_height()) / 2

        draw_surf.blit(self.shadow, (self.rect.x - camera_offset[0] - (self.shadow.get_width() - self.image.get_width()) / 2, self.rect.y - camera_offset[1] + self.image.get_height()))
        draw_surf.blit(img, (render_x, render_y))
    
    def move(self, tiles):
        if self.vel.length() > 0:
            self.vel = self.vel.normalize()

        speed = self.speed
        self.total_vel = self.vel * speed + self.ext_vel

        self.y += self.total_vel.y * self.dt
        self.rect.y = self.y
        self.vertical_collision(tiles)
        self.rect.y = self.y

        self.x += self.total_vel.x * self.dt
        self.rect.x = self.x
        self.horizontal_collision(tiles)
        self.rect.x = self.x

    def vertical_collision(self, tiles):
        for tile in tiles:

            if tile.rect.colliderect(self.rect):

                if self.total_vel.y > 0:
                    self.y = tile.rect.top - self.rect.h
                    self.vel.y = 0
                    self.ext_vel.y = 0
                    self.total_vel.y = 0
                
                elif self.total_vel.y < 0:
                    self.y = tile.rect.bottom
                    self.vel.y = 0
                    self.ext_vel.y = 0
                    self.total_vel.y = 0

    def horizontal_collision(self, tiles):
        for tile in tiles:

            if tile.rect.colliderect(self.rect):
            
                if self.total_vel.x > 0:
                    self.x = tile.rect.left - self.rect.w
                    self.vel.x = 0
                    self.ext_vel.x = 0
                    self.total_vel.x = 0
                
                elif self.total_vel.x < 0:
                    self.x = tile.rect.right
                    self.vel.x = 0
                    self.ext_vel.x = 0
                    self.total_vel.x = 0
        
    def scale(self, scale_x=1.0, scale_y=1.0):
        self.scale_x = scale_x
        self.scale_y = scale_y

    def rescale(self):
        speed = 0.1
        self.scale_x += (1.0 - self.scale_x) * speed * self.dt
        self.scale_y += (1.0 - self.scale_y) * speed * self.dt
        
    def update(self, delta_time):
        self.dt = delta_time
        self.rescale()

        self.ext_vel.x += (0 - self.ext_vel.x) * self.dt
        self.ext_vel.y += (0 - self.ext_vel.y) * self.dt
        
        if abs(self.ext_vel.x) < 0.001:
            self.ext_vel.x = 0
        if abs(self.ext_vel.y) < 0.001:
            self.ext_vel.y = 0
        
        self.damage_timer -= self.dt
        self.flicker_timer -= self.dt