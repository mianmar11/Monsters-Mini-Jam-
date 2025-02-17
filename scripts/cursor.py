import pygame

class Cursor:
    def __init__(self, tile_size):
        self.tile_size = tile_size

        self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(self.image, 'white', (0, 0, self.tile_size/6, self.tile_size/4)) # topleft
        pygame.draw.rect(self.image, 'white', (0, 0, self.tile_size/4, self.tile_size/6)) # topleft

        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1.5, self.image.get_height() * 1.5))

        self.angle = 0

    def draw(self, draw_surf, pos):
        surf = pygame.transform.rotozoom(self.image, self.angle, 1)

        render_x = pos[0] - surf.get_width()/2
        render_y = pos[1] - surf.get_height()/2

        draw_surf.blit(surf, (render_x, render_y)) # topleft arrow
        for i in [90, 180, 270]:
            img = pygame.transform.rotozoom(self.image, self.angle + i, 1)
            render_x = pos[0] - img.get_width()/2
            render_y = pos[1] - img.get_height()/2
            draw_surf.blit(img, (render_x, render_y))

    def update(self, delta_time, draw_surf, pos):
        self.dt = delta_time

        self.angle += self.dt
        self.draw(draw_surf, pos)
