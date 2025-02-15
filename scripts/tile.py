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
    
    def draw(self, draw_surf, camera_offset):
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]

        draw_surf.blit(self.image, (render_x, render_y))

def auto_tile(tiles, tile_size):
    tiles = tiles.copy()
    AUTOTILE_MAP = {
        # rects which will render on the image so that they will show the edge highlights
        tuple(sorted([(0, 1), (1, 0)])): [(0, 0, tile_size, tile_size/8), (0, 0, tile_size/8, tile_size)], # topleft
        tuple(sorted([(0, 1), (1, 0), (-1, 0)])): [(0, 0, tile_size, tile_size/8)], # middletop
        tuple(sorted([(0, 1), (-1, 0)])): [(0, 0, tile_size, tile_size/8), (tile_size - tile_size/8, 0, tile_size/8, tile_size)], # topright

        tuple(sorted([(0, -1), (1, 0), (0, 1)])): [(0, 0, tile_size/8, tile_size)], # left
        tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0)])): [], # middle
        tuple(sorted([(0, 1), (-1, 0), (0, -1)])): [(tile_size - tile_size/8, 0, tile_size/8, tile_size)], # right

        tuple(sorted([(0, -1), (1, 0)])): [(0, tile_size - tile_size/8, tile_size, tile_size/8), (0, 0, tile_size/8, tile_size)], # bottomleft
        tuple(sorted([(0, -1), (-1, 0), (1, 0)])): [(0, tile_size - tile_size/8, tile_size, tile_size/8)], # bottom
        tuple(sorted([(0, -1), (-1, 0)])): [(0, tile_size - tile_size/8, tile_size, tile_size/8), (tile_size - tile_size/8, 0, tile_size/8, tile_size)], # bottomright
       
        # vertical tiles
        tuple(sorted([(0, 1)])): [(0, 0, tile_size, tile_size/8), (0, 0, tile_size/8, tile_size), (tile_size - tile_size/8, 0, tile_size/8, tile_size)], # top
        tuple(sorted([(0, -1), (0, 1)])): [(0, 0, tile_size/8, tile_size), (tile_size - tile_size/8, 0, tile_size/8, tile_size)], # middle
        tuple(sorted([(0, -1)])): [(0, 0, tile_size/8, tile_size), (0, tile_size - tile_size/8, tile_size, tile_size/8), (tile_size - tile_size/8, 0, tile_size/8, tile_size)], # bottom

        # horizontal tiles
        tuple(sorted([(1, 0)])): [(0, 0, tile_size/8, tile_size), (0, 0, tile_size, tile_size/8), (0, tile_size - tile_size/8, tile_size, tile_size/8)], # left
        tuple(sorted([(1, 0), (-1, 0)])): [(0, 0, tile_size, tile_size/8), (0, tile_size - tile_size/8, tile_size, tile_size/8)], # middle
        tuple(sorted([(-1, 0)])): [(0, 0, tile_size, tile_size/8), (0, tile_size - tile_size/8, tile_size, tile_size/8), (tile_size - tile_size/8, 0, tile_size/8, tile_size)], # right,

        # single tiles
        (): [(0, 0, tile_size, tile_size/8), (0, 0, tile_size/8, tile_size), (tile_size - tile_size/8, 0, tile_size/8, tile_size), (0, tile_size - tile_size/8, tile_size, tile_size/8)], # single
    }

    for pos in tiles:
        if tiles[pos].tile_type not in ['dirt', 'dirt2']:
            continue
        try:
            neighbors = set()

            for shift in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_offset = (pos[0] + shift[0], pos[1] + shift[1])

                if tiles[new_offset].tile_type in ['dirt', 'dirt2']:
                    neighbors.add(shift)
            
            neighbors = tuple(sorted(neighbors))

            if neighbors in AUTOTILE_MAP:
                for rect in AUTOTILE_MAP[neighbors]:
                    pygame.draw.rect(tiles[pos].image, 'white', rect)
    
        except KeyError:
            pass
        
    return tiles
