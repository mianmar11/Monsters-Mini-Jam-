import pygame

class Tile:
    def __init__(self, tile_type, tile_size, pos):
        self.tile_type = tile_type
        self.tile_size = tile_size
        self.pos = pos[0] * self.tile_size, pos[1] * self.tile_size

        self.image = pygame.Surface((self.tile_size, self.tile_size)).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)

        if self.tile_type == 'grass':
            self.image.fill('#32a852')
        elif self.tile_type == 'dark grass':
            self.image.fill('#146138')
    
    def draw(self, draw_surf, camera_offset):
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]

        draw_surf.blit(self.image, (render_x, render_y))
