import pygame, random, math
from pygame.math import Vector2 as vec2

from scripts.terrain import generate_world_data
from scripts.tile import Tile, auto_tile

from scripts.entities.player import Player
from scripts.entities.bullet import BulletManager
from scripts.entities.enemy import EnemyManager
from scripts.weapon.ranged import RangeWeapon
from scripts.camera import Camera

from scripts.utils import *

class Game:
    def __init__(self, window):
        self.window = window
        self.WIDTH, self.HEIGHT = self.window.get_size()

        self.tile_size = 16
        self.ground_tiles = {}
        self.tiles = {}
        
        self.chunk_size = [14, 12]
        self.chunk_surfs = {} # cached tiles on chunk surfaces only used for rendering

        self.WORLD_MAP_SIZE = [self.WIDTH//16 * 5, self.HEIGHT//16 * 5]

        self.load()
        self.ground_tiles = self.chunking(self.ground_tiles)
        self.tiles = self.chunking(self.tiles)

        spawn_area =  [pos for pos, tile in self.ground_tiles.items() if tile.tile_type not in ('air', 'edge')]
        self.spawn_area = [pos for pos in spawn_area if self.tiles[pos].tile_type in ('air', 'edge')]
        spawn_point = random.choice([pos for pos in self.spawn_area if ((pos[0] - self.WORLD_MAP_SIZE[0]//2)**2 + (pos[1] - self.WORLD_MAP_SIZE[1]//2)**2)**0.5 < self.WORLD_MAP_SIZE[1]/3])
        self.player = Player(self.tile_size, spawn_point)

        self.enemy_manager = EnemyManager(self.tile_size)
        self.spawn_enemies(10)

        self.weapon = RangeWeapon(self.tile_size)
        self.bullet_manager = BulletManager(self.tile_size)

        self.camera = Camera((self.WIDTH, self.HEIGHT), self.tile_size)
    
    def spawn_enemies(self, amount):
        for i in range(amount):
            self.enemy_manager.spawn(random.choice(self.spawn_area))

    def chunking(self, tiles):
        tiles = tiles.copy()
        for pos in tiles:
            chunk_offset = (pos[0] // self.chunk_size[0], pos[1] // self.chunk_size[1])
            if chunk_offset not in self.chunk_surfs:
                self.chunk_surfs[chunk_offset] = pygame.Surface((self.chunk_size[0] * self.tile_size, self.chunk_size[1] * self.tile_size), pygame.SRCALPHA).convert_alpha()
            
            tiles[pos].draw(self.chunk_surfs[chunk_offset], [chunk_offset[0] * self.chunk_size[0] * self.tile_size, chunk_offset[1] * self.chunk_size[1] * self.tile_size])

        return tiles

    def load(self):
        seed = random.randint(0, 256)
        terrain_data = {(-0.3, 1): 'dirt', (-0.5, -0.3): 'dirt2', (-1, -0.5): 'air'} # map data
        tile_data = {(0.2, 1): 'dirt', (0, 0.2): 'dirt2', (-1, 0): 'air'} # tile data
        
        world_data = generate_world_data(self.WORLD_MAP_SIZE, terrain_data, seed)
        obj_data = generate_world_data(self.WORLD_MAP_SIZE, tile_data, seed)

        datas = [world_data, obj_data]
        offices = [self.ground_tiles, self.tiles]

        for i, data in enumerate(datas): # loop through world data and obj data
            for pos in data:
                terrain_type = data[pos]

                if terrain_type == 'dirt' or terrain_type == 'dirt2':
                    
                    # if there is no tile (void | out of world) on top of current tile, make the current tile air tile
                    if (pos[0], pos[1] - 1) not in data:
                        terrain_type = 'air'
                    
                    # if there is no tile (void | out of world) underneath current tile, make the current tile edge tile
                    if (pos[0], pos[1] + 1) not in data:
                        terrain_type = 'edge' if (pos[0], pos[1] - 1) in data and data[(pos[0], pos[1] - 1)] in ['dirt', 'dirt2'] else 'air'
                    
                    # if there is tile underneath dirt tile and it is air tile, make the current tile edge tile
                    elif data[(pos[0], pos[1] + 1)] == 'air':
                        terrain_type = 'edge' if (pos[0], pos[1] - 1) in data and data[(pos[0], pos[1] - 1)] in ['dirt', 'dirt2'] else 'air'

                    # terrain_type = 'dirt2'
            
                offices[i][pos] = Tile(terrain_type, self.tile_size, pos)
            
        self.ground_tiles = auto_tile(self.ground_tiles, self.tile_size)
        self.tiles = auto_tile(self.tiles, self.tile_size)

    def draw(self, camera_offset):
        for chunk_offset in self.chunk_surfs:
            # print(i[0] * self.chunk_size[0] * self.tile_size, i[1] * self.chunk_size[1] * self.tile_size)
            self.window.blit(self.chunk_surfs[chunk_offset], [chunk_offset[0] * self.chunk_size[0] * self.tile_size - camera_offset[0], chunk_offset[1] * self.chunk_size[1] * self.tile_size - camera_offset[1]])

        self.enemy_manager.draw(self.window, camera_offset)
        self.player.draw(self.window, camera_offset)
        self.bullet_manager.draw(self.window, camera_offset)

    def entity_bullet_collision(self):
        for entity in self.enemy_manager.enemies:
            for bullet in self.bullet_manager.bullets:

                if entity.rect.colliderect(bullet.rect):
                    
                    if entity.deduct_health():
                        self.camera.start_shake(4)
                        entity.ext_vel = vec2(1, 0).rotate(bullet.angle).normalize() * 4 # knockback
                        entity.get_pursue()

                        if entity.health <= 0:
                            self.enemy_manager.enemies.remove(entity)

                        bullet.piercing -= 1
                        if bullet.piercing <= 0:
                            self.bullet_manager.bullets.remove(bullet)
                            break

            if entity.rect.colliderect(self.player.rect):
                if self.player.deduct_health():
                    self.camera.start_shake(6)
                            
                    dx = entity.rect.centerx - self.player.rect.centerx
                    dy = entity.rect.centery - self.player.rect.centery

                    angle = math.degrees(math.atan2(dy, dx))

                    self.player.ext_vel = vec2(-1, 0).rotate(angle).normalize() * self.tile_size

    def update(self, delta_time):
        self.dt = delta_time
        mx, my = pygame.mouse.get_pos()
        mbutton = pygame.mouse.get_pressed()
                
        camera_offset = self.camera.offset(self.player, self.dt, mx, my)

        angle = math.degrees(math.atan2(my + camera_offset[1] - self.player.rect.centery, mx + camera_offset[0] - self.player.rect.centerx))

        if mbutton[0]:
            if self.weapon.shoot():
                self.bullet_manager.add_bullet(self.player.rect.center, angle + random.randint(-3, 3))

                self.player.ext_vel = vec2(-1, 0).rotate(angle).normalize() * 1 # knockback
        
        self.player.update(self.dt)
        player_offset = get_offset(self.player, self.tile_size)
        collide_tiles = []
        for offset in [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
            tile_offset = (player_offset[0] + offset[0], player_offset[1] + offset[1])
            if tile_offset in self.ground_tiles:
                collide_tiles.append(self.ground_tiles[tile_offset]) if self.ground_tiles[tile_offset].tile_type in ['air', 'edge'] else None
            if tile_offset in self.tiles:
                collide_tiles.append(self.tiles[tile_offset]) if self.tiles[tile_offset].tile_type not in ['air', 'edge'] else None
        self.player.move(collide_tiles)

        self.enemy_manager.update(self.dt, self.player, self.ground_tiles, self.tiles)

        self.weapon.update(self.dt)
        self.bullet_manager.update(self.dt, self.tiles)

        self.entity_bullet_collision()

        self.draw(camera_offset)

    def event_controls(self, event):
        if event.type == pygame.KEYUP:
            self.player.keyup(event.key)

        if event.type == pygame.KEYDOWN:
            self.player.keydown(event.key)
