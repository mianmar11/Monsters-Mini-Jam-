import pygame

class Tile:
    def __init__(self, tile_type, tile_size, pos):
        self.tile_type = tile_type
        self.tile_size = tile_size
        self.pos = pos[0] * self.tile_size, pos[1] * self.tile_size

        self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)

        if self.tile_type == 'dirt': # white dirt
            self.image.fill('#d9a066')
        elif self.tile_type == 'dirt2': # darker dirt
            self.image.fill('#bc8750')
        elif self.tile_type == 'edge': # dark edge 
            self.image.fill('#663931')
        
        if self.tile_type == 'edge':
            self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()*0.75))
    
    def draw(self, draw_surf, camera_offset):
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]

        draw_surf.blit(self.image, (render_x, render_y))

def auto_tile(tiles, tile_size):
    tiles = tiles.copy()
    AUTOTILE_MAP = {
        # rects which will render on the image so that they will show the edge highlights
        tuple((0, -1)): [(0, 0, tile_size, tile_size/8)], # middletop
        tuple((-1, 0)): [(0, 0, tile_size/8, tile_size)], # left
        tuple((1, 0)): [(tile_size - tile_size/8, 0, tile_size/8, tile_size)], # right
        tuple((0, 1)): [(0, tile_size - tile_size/8, tile_size, tile_size/8)], # bottom
        }

    for pos in tiles:
        if tiles[pos].tile_type not in ['dirt', 'dirt2']:
            continue
        
        try:
            for shift in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_offset = (pos[0] + shift[0], pos[1] + shift[1])

                if tiles[new_offset].tile_type in ['air', 'edge']:
                    for rect in AUTOTILE_MAP[shift]:
                        pygame.draw.rect(tiles[pos].image, 'white', rect)
    
        except KeyError:
            pass
        
    return tiles