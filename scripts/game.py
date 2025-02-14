import pygame

from scripts.terrain import generate_world_data
from scripts.tile import Tile

from scripts.entities.player import Player
from scripts.camera import Camera

class Game:
    def __init__(self, window):
        self.window = window
        self.WIDTH, self.HEIGHT = self.window.get_size()

        self.tile_size = 16
        self.tiles = {}
        
        self.chunk_size = [14, 12]
        self.chunk_surfs = {} # cached tiles on chunk surfaces only used for rendering

        self.WORLD_MAP_SIZE = [self.WIDTH//self.tile_size * 3, self.HEIGHT//self.tile_size * 3]

        self.load()

        self.player = Player(self.tile_size, (0, 0))

        self.camera = Camera((self.WIDTH, self.HEIGHT))
    
    def load(self):
        '''generate the world and tile it'''
        world_data = generate_world_data(self.WORLD_MAP_SIZE)

        for pos in world_data:
            chunk_offset = (pos[0] // self.chunk_size[0], pos[1] // self.chunk_size[1])
            if chunk_offset not in self.chunk_surfs:
                self.chunk_surfs[chunk_offset] = pygame.Surface((self.chunk_size[0] * self.tile_size, self.chunk_size[1] * self.tile_size), pygame.SRCALPHA).convert_alpha()

            self.tiles[pos] = Tile(world_data[pos], self.tile_size, pos)
            self.tiles[pos].draw(self.chunk_surfs[chunk_offset], [chunk_offset[0] * self.chunk_size[0] * self.tile_size, chunk_offset[1] * self.chunk_size[1] * self.tile_size])

    def draw(self, camera_offset):
        for chunk_offset in self.chunk_surfs:
            # print(i[0] * self.chunk_size[0] * self.tile_size, i[1] * self.chunk_size[1] * self.tile_size)
            self.window.blit(self.chunk_surfs[chunk_offset], [chunk_offset[0] * self.chunk_size[0] * self.tile_size - camera_offset[0], chunk_offset[1] * self.chunk_size[1] * self.tile_size - camera_offset[1]])

        self.player.draw(self.window, camera_offset)

    def update(self, delta_time):
        self.dt = delta_time

        camera_offset = self.camera.offset(self.player, self.dt)
        
        self.player.update(self.dt)

        self.draw(camera_offset)

    def event_controls(self, event):
        if event.type == pygame.KEYUP:
            self.player.keyup(event.key)

        if event.type == pygame.KEYDOWN:
            self.player.keydown(event.key)
