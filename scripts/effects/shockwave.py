import pygame

class Shockwave:
    def __init__(self, pos, tile_size):
        self.pos = pos
        self.tile_size = tile_size

        self.radius = 0
        self.width = 4
    
    def draw(self, draw_surf, camera_offset):
        render_x = self.pos[0] - camera_offset[0]
        render_y = self.pos[1] - camera_offset[1]

        pygame.draw.circle(draw_surf, (10, 10, 10), (render_x, render_y + 2), self.radius, int(self.width))
        pygame.draw.circle(draw_surf, '#ffeb79', (render_x, render_y), self.radius, int(self.width))

    def update(self, delta_time):
        self.dt = delta_time

        self.radius += (self.tile_size * 4 - self.radius) * 0.1 * self.dt
        if round(self.radius) >= self.tile_size * 4:
            self.width += (0 - self.width) * 0.5 * self.dt
            if self.width < 1:
                return True
        return