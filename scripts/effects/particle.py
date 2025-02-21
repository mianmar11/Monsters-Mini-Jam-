import random, pygame
from pygame.math import Vector2 as vec2

class Particle:
    def __init__(self, pos, angle, tile_size, collided_obj):
        self.ori_pos = pos
        self.pos = list(pos)
        self.tile_size = tile_size
        self.angle = angle # the angle which bullet went

        self.ori_size = self.tile_size + random.randint(-self.tile_size/4, 0)
        self.size = self.ori_size

        if collided_obj == None:
            self.color = random.choices(["yellow", 'white'], weights=[1, 5], k=1)[0]
        elif collided_obj.tile_type in ['dirt', 'dirt2']:
            self.color = random.choice(['#d9a066', '#bc8750', '#663931'])

        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.fill(self.color)

        self.shadow_image = pygame.mask.from_surface(self.image)
        self.shadow_image = self.shadow_image.to_surface(unsetcolor=(255, 255, 255, 255), setcolor=(0, 0, 0, 255))

        self.vel = vec2(random.choices([1, -1], weights=[1, 20], k=1)[0], 0).rotate(self.angle).normalize() * random.randint(2, 6)

        # self.color = random.choice(['#a27c54', '#c99a6a', '#bb9064'])
    
    def draw_shadow(self, draw_surf, camera_offset):
        img = pygame.transform.scale(self.shadow_image, (self.size, self.size))
        img = pygame.transform.rotate(img, self.angle)

        render_x = self.pos[0] - img.get_width() / 2 - camera_offset[0] 
        render_y = self.pos[1] - img.get_height() / 2 - camera_offset[1] + self.image.get_height() 

        draw_surf.blit(img, (render_x, render_y))
        
        # pygame.draw.circle(draw_surf, (0, 0, 0), (render_x, render_y), self.radius)

    def draw(self, draw_surf, camera_offset):
        img = pygame.transform.scale(self.image, (self.size, self.size))
        img = pygame.transform.rotate(img, self.angle)

        render_x = self.pos[0] - img.get_width() / 2 - camera_offset[0] 
        render_y = self.pos[1] - img.get_height() / 2 - camera_offset[1] 

        draw_surf.blit(img, (render_x, render_y))
        
        # pygame.draw.circle(draw_surf, self.color, (render_x, render_y), self.radius)
    
    def update(self, delta_time):
        self.dt = delta_time

        self.vel.x += (0 - self.vel.x) * 0.1 * self.dt
        self.vel.y += (0 - self.vel.y) * 0.1 * self.dt

        self.pos[0] += self.vel.x * self.dt
        self.pos[1] += self.vel.y * self.dt

        self.angle += 5 * self.dt

        self.size -= 0.3 * self.dt
        if self.size <= 0:
            return True
        return
