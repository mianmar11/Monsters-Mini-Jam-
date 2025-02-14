import pygame    

class Entity:
    def __init__(self, tile_size, pos):
        self.tile_size = tile_size
        self.x, self.y = pos[0] * self.tile_size, pos[1] * self.tile_size

        self.image = pygame.Surface((self.tile_size, self.tile_size)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.image.fill('blue')

    def draw(self, draw_surf, camera_offset):
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]

        draw_surf.blit(self.image, (render_x, render_y))
    
    def update(self, delta_time):
        self.dt = delta_time
        