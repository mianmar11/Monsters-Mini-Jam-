import pygame

from scripts.utilities.utils import *

class Minimap:
    def __init__(self, world_size, chunk_size, ground_data, tile_data, tile_size):
        self.tile_size = tile_size
        self.chunk_size = chunk_size

        self.world_map = {}

        for layer, data in enumerate([ground_data, tile_data]):
            for pos in data:
                if data[pos] not in ['air', 'edge']:
                    chunk_pos = (pos[0]//chunk_size[0], pos[1]//chunk_size[1])
                    if chunk_pos not in self.world_map:
                        self.world_map[chunk_pos] = pygame.Surface(chunk_size, pygame.SRCALPHA).convert_alpha()
                        self.world_map[chunk_pos].set_alpha(128)
                    
                    # print((pos[0] - chunk_size[0] * chunk_pos[0], pos[1] - chunk_size[1] * chunk_pos[1]))
                    if layer == 0:
                        pygame.draw.rect(self.world_map[chunk_pos], (128, 128, 128), (pos[0] - chunk_size[0] * chunk_pos[0], pos[1] - chunk_size[1] * chunk_pos[1], 1, 1))
                    else:
                        pygame.draw.rect(self.world_map[chunk_pos], (160, 160, 160), (pos[0] - chunk_size[0] * chunk_pos[0], pos[1] - chunk_size[1] * chunk_pos[1], 1, 1))
        
    def draw(self, draw_surf, chunk_offset, camera_offset):
        draw_surf.blit(self.world_map[chunk_offset], (320 + camera_offset[0]//self.tile_size - chunk_offset[0] * self.chunk_size[0], camera_offset[1]//self.tile_size - chunk_offset[1] * self.chunk_size[1]))
        