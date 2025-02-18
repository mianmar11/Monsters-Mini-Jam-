import random, pygame
from pygame.math import Vector2 as vec2

class Particle:
    def __init__(self, pos, angle, tile_size):
        self.ori_pos = pos
        self.pos = list(pos)
        self.tile_size = tile_size
        self.angle = angle # the angle which bullet went

        self.vel = vec2(1, 0).rotate(self.angle).normalize() * 4

        self.radius = random.randint(self.tile_size//2, self.tile_size)
        self.color = random.choice(['#a27c54', '#c99a6a', '#bb9064'])
    
    def draw(self, draw_surf, camera_offset):
        render_x = self.pos[0] - camera_offset[0]
        render_y = self.pos[1] - camera_offset[1]
        
        pygame.draw.circle(draw_surf, (10, 10, 10), (render_x, render_y + 2), self.radius)
        pygame.draw.circle(draw_surf, self.color, (render_x, render_y), self.radius)
    
    def update(self, delta_time):
        self.dt = delta_time

        self.vel.x += (0 - self.vel.x) * 0.3 * self.dt
        self.vel.y += (0 - self.vel.y) * 0.3 * self.dt

        self.pos[0] += self.vel.x * self.dt
        self.pos[1] += self.vel.y * self.dt

        self.radius -= 0.5 * self.dt
        if self.radius < 1:
            return True
        return
