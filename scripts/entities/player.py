import pygame
from pygame.math import Vector2 as vec2

from scripts.entities.entity import Entity

class Player(Entity):
    def __init__(self, tile_size, pos):
        super().__init__(tile_size, pos)

        self.angle = 0 # for rendering only

        self.directions = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        self.speed = 2.4

        self.damage_taken_cooldown = 60
    
    def controller(self, controller, threshold):
        x = controller.get_axis(0)
        y = controller.get_axis(1)
        self.vel.x = x if abs(x) > threshold else 0
        self.vel.y = y if abs(y) > threshold else 0

    def keydown(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.vel.y = -1
        elif key[pygame.K_s]:
            self.vel.y = 1

        if key[pygame.K_d]:
            self.vel.x = 1
        elif key[pygame.K_a]:
            self.vel.x = -1
    
    def keyup(self):
        key = pygame.key.get_just_released()
        if key[pygame.K_w]:
            self.vel.y = 0
        elif key[pygame.K_s]:
            self.vel.y = 0

        if key[pygame.K_d]:
            self.vel.x = 0
        elif key[ pygame.K_a]:
            self.vel.x = 0

    def update(self, delta_time):
        self.dt = delta_time
        self.rescale()
        self.keydown()
        self.keyup()

        self.ext_vel.x += (0 - self.ext_vel.x) * 0.5 * self.dt
        self.ext_vel.y += (0 - self.ext_vel.y) * 0.5 * self.dt
        
        if abs(self.ext_vel.x) < 0.001:
            self.ext_vel.x = 0
        if abs(self.ext_vel.y) < 0.001:
            self.ext_vel.y = 0
        
        self.damage_timer -= self.dt
        self.flicker_timer -= self.dt
 
    def draw_shadow(self, draw_surf, camera_offset):
        shadow_img = self.shadow.copy()
        # shadow_img = pygame.transform.rotate(self.shadow.copy(), self.angle)

        render_x = self.rect.x - camera_offset[0] - (shadow_img.get_width() - self.image.get_width()) / 2
        render_y = self.rect.y - camera_offset[1] + self.image.get_height() - self.shadow.get_height()/4
        
        draw_surf.blit(shadow_img, (render_x, render_y), special_flags=pygame.BLEND_RGBA_MULT)
    
    def draw(self, draw_surf, camera_offset):
        if self.vel.x < 0: # tilt left and stretch if moving left
            self.angle += (10 - self.angle) * 0.3 * self.dt
            self.scale_x += (0.9 - self.scale_x) * 0.5 * self.dt
            self.scale_y += (1.1 - self.scale_y) * 0.5 * self.dt
        elif self.vel.x > 0: # tilt right and stretch if moving right
            self.angle += (-10 - self.angle) * 0.3 * self.dt
            self.scale_x += (0.9 - self.scale_x) * 0.5 * self.dt
            self.scale_y += (1.1 - self.scale_y) * 0.5 * self.dt
        else: # do not tilt
            self.angle += (0 - self.angle) * 0.3 * self.dt
        
        if self.vel.y < 0: # stretch if moving upwards
            self.scale_x += (0.8 - self.scale_x) * 0.5 * self.dt
            self.scale_y += (1.2 - self.scale_y) * 0.5 * self.dt
        elif self.vel.y > 0: # squish if moving downwards
            self.scale_x += (1.2 - self.scale_x) * 0.5 * self.dt
            self.scale_y += (0.8 - self.scale_y) * 0.5 * self.dt    
        
        scale_x = self.scale_x
        scale_y = self.scale_y

        img = pygame.transform.scale(self.image.copy(), (self.image.get_width() * scale_x, self.image.get_height() * scale_y))
        
        if self.flicker_timer > 0 and int(self.flicker_timer) % 6 == 0:
            img.fill('red')
        
        img = pygame.transform.rotate(img, self.angle)

        render_x = self.rect.x - camera_offset[0] - (img.get_width() - self.image.get_width()) / 2
        render_y = self.rect.y - camera_offset[1] - (img.get_width() - self.image.get_height()) / 2

        draw_surf.blit(img, (render_x, render_y))
    