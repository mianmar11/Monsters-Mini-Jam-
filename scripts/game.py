import pygame, random, math
from pygame.math import Vector2 as vec2

from scripts.terrain import generate_world_data
from scripts.tile import Tile, auto_tile

from scripts.entities.player import Player
from scripts.entities.bullet import BulletManager
from scripts.entities.enemy import EnemyManager
from scripts.weapon.ranged import RangeWeapon
from scripts.shockwave import Shockwave
from scripts.camera import Camera
from scripts.particle import Particle
from scripts.cursor import Cursor

from scripts.text import TextManager
from scripts.utils import *
from scripts.sfx import SFX

class Game:
    def __init__(self, window):
        self.window = window
        self.WIDTH, self.HEIGHT = self.window.get_size()
        self.chunk_size = [14, 12]
        self.WORLD_MAP_SIZE = [self.WIDTH//16 * 5, self.HEIGHT//16 * 5]
        self.fade = self.window.copy()

        self.tile_size = 16

        self.cursor = Cursor(self.tile_size)
        self.text_manager = TextManager(self.tile_size, (self.WIDTH, self.HEIGHT))
        self.camera = Camera((self.WIDTH, self.HEIGHT), self.tile_size)
        
        self.shockwaves = []
        self.particles = []

        self.sfx = SFX()
        self.sfx.play('music', loop=-1)

        self.chunk_surfs = {} # cached tiles on chunk surfaces only used for rendering
        self.ground_tiles = {}
        self.tiles = {}

        self.load()

        spawn_area =  [pos for pos, tile in self.ground_tiles.items() if tile.tile_type not in ('air', 'edge')]
        self.spawn_area = [pos for pos in spawn_area if self.tiles[pos].tile_type in ('air', 'edge')]
        spawn_point = random.choice([pos for pos in self.spawn_area if ((pos[0] - self.WORLD_MAP_SIZE[0]//2)**2 + (pos[1] - self.WORLD_MAP_SIZE[1]//2)**2)**0.5 < self.WORLD_MAP_SIZE[1]/3])
        self.player = Player(self.tile_size, spawn_point)

        self.game_started = False
        self.lost = False
        self.upgraded = False
        self.wave = 1
        self.enemy_manager = EnemyManager(self.tile_size)
        self.enemy_spawn_rate = 10
        self.spawn_enemies(self.enemy_spawn_rate)

        self.weapon = RangeWeapon(self.tile_size)
        self.bullet_manager = BulletManager(self.tile_size)

        self.radius = 0
        self.fade_in = False
        self.text_manager.queue_text(f"Wave {self.wave}", self.text_manager.BIG_FONT, {'center': (self.WIDTH/2, self.HEIGHT/2)})
    
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

    def restart(self):
        self.chunk_surfs = {} # cached tiles on chunk surfaces only used for rendering
        self.ground_tiles = {}
        self.tiles = {}

        self.load()

        spawn_area =  [pos for pos, tile in self.ground_tiles.items() if tile.tile_type not in ('air', 'edge')]
        self.spawn_area = [pos for pos in spawn_area if self.tiles[pos].tile_type in ('air', 'edge')]
        spawn_point = random.choice([pos for pos in self.spawn_area if ((pos[0] - self.WORLD_MAP_SIZE[0]//2)**2 + (pos[1] - self.WORLD_MAP_SIZE[1]//2)**2)**0.5 < self.WORLD_MAP_SIZE[1]/3])
        self.player = Player(self.tile_size, spawn_point)

        self.game_started = False
        self.lost = False
        self.upgraded = False
        self.wave = 1
        self.enemy_manager = EnemyManager(self.tile_size)
        self.enemy_spawn_rate = 10
        self.spawn_enemies(self.enemy_spawn_rate)

        self.weapon = RangeWeapon(self.tile_size)
        self.bullet_manager = BulletManager(self.tile_size)

        self.radius = 0
        self.fade_in = False
        self.text_manager.queue_text(f"Wave {self.wave}", self.text_manager.BIG_FONT, {'center': (self.WIDTH/2, self.HEIGHT/2)})

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
        
        self.chunking(self.ground_tiles)
        self.chunking(self.tiles)

    def draw(self, camera_offset):
        for chunk_offset in self.chunk_surfs:
            # print(i[0] * self.chunk_size[0] * self.tile_size, i[1] * self.chunk_size[1] * self.tile_size)
            self.window.blit(self.chunk_surfs[chunk_offset], [chunk_offset[0] * self.chunk_size[0] * self.tile_size - camera_offset[0], chunk_offset[1] * self.chunk_size[1] * self.tile_size - camera_offset[1]])

        self.enemy_manager.draw(self.window, camera_offset)
        self.player.draw(self.window, camera_offset)
        self.bullet_manager.draw(self.window, camera_offset)

        for shockwave in self.shockwaves.copy():
            shockwave.draw(self.window, camera_offset)
            if shockwave.update(self.dt):
                self.shockwaves.remove(shockwave)
        
        for particle in self.particles.copy():
            particle.draw(self.window, camera_offset)
            if particle.update(self.dt):
                self.particles.remove(particle)

        # render player health
        for i in range(self.player.health):
            pygame.draw.rect(self.window, 'red', (10 + i * self.tile_size, 10, self.tile_size/1.5, self.tile_size/1.5))
            pygame.draw.rect(self.window, 'white', (10 + i * self.tile_size, 10, self.tile_size/1.5, self.tile_size/1.5), 1)

    def minimap(self):
        pygame.draw.rect(self.window, (0, 0, 0), (self.WIDTH - self.WORLD_MAP_SIZE[0], 0, self.WORLD_MAP_SIZE[0], self.WORLD_MAP_SIZE[1]), 1)
        for entity in self.enemy_manager.enemies:
            enemy_offset = get_offset(entity, self.tile_size)
            pygame.draw.rect(self.window, 'white', (enemy_offset[0] + self.WIDTH - self.WORLD_MAP_SIZE[0], enemy_offset[1], 2, 2))
        player_offset = get_offset(self.player, self.tile_size)
        pygame.draw.rect(self.window, 'blue', (player_offset[0] + self.WIDTH - self.WORLD_MAP_SIZE[0], player_offset[1], 2, 2))

    def entity_bullet_collision(self):
        for entity in self.enemy_manager.enemies:
            for bullet in self.bullet_manager.bullets:

                if entity.rect.colliderect(bullet.rect):
                    
                    if entity.deduct_health(bullet.damage):
                        self.camera.start_shake(4)
                        self.sfx.play("hit")
                        self.particles += [Particle((entity.rect.centerx + random.randint(8, 10), entity.rect.centery + random.randint(8, 10)), bullet.angle + random.randint(10, 30) * random.choice([-1, 1]), self.tile_size) for i in range(random.randint(1, 4))]

                        entity.ext_vel = vec2(1, 0).rotate(bullet.angle).normalize() * 4 # knockback
                        entity.get_pursue()

                        if entity.health <= 0:
                            self.shockwaves.append(Shockwave(entity.rect.center, self.tile_size))
                            self.enemy_manager.enemies.remove(entity)

                        bullet.piercing -= 1
                        if bullet.piercing <= 0:
                            self.bullet_manager.bullets.remove(bullet)
                            break

            if entity.rect.colliderect(self.player.rect):
                if self.player.deduct_health(entity.damage):
                    self.camera.start_shake(6)
                    self.sfx.play("hit")
                            
                    dx = entity.rect.centerx - self.player.rect.centerx
                    dy = entity.rect.centery - self.player.rect.centery

                    angle = math.degrees(math.atan2(dy, dx))

                    self.player.ext_vel = vec2(-1, 0).rotate(angle).normalize() * self.tile_size

                    self.game_state()

    def tile_bullet_collision(self):
        for bullet in self.bullet_manager.bullets:
            destroy = bullet.destroy()
            collided = bullet.collision(self.tiles.get(get_offset(bullet, self.tile_size), None))
            if destroy or collided:
                self.particles += [Particle((bullet.rect.centerx + random.randint(8, 10), bullet.rect.centery + random.randint(8, 10)), bullet.angle + random.randint(10, 30) * random.choice([-1, 1]), self.tile_size) for i in range(random.randint(1, 4))]
                self.bullet_manager.bullets.remove(bullet)

    def game_state(self):
        if self.player.health <= 0:
            self.lost = True
            self.fade_in = True
            self.shockwaves.append(Shockwave(self.player.rect.center, self.tile_size))

    def upgrade(self):
        if len(self.enemy_manager.enemies) <= 0:
            chance = random.randint(0, 2)
            if self.wave % 4 == 0 and self.upgraded == False:
                if chance == 1:
                    if self.bullet_manager.damage < 6:
                        self.bullet_manager.damage += 0.5
                        'Bullets deal more damage'
                        self.text_manager.queue_text("Bullets Damage: +0.5", self.text_manager.BIG_FONT, {'center': (self.WIDTH/2, self.HEIGHT/2 + self.tile_size/2)}, 180)
                elif chance == 2:
                    if self.weapon.cooldown > 4:
                        self.weapon.cooldown -= 1
                        'Reduced weapon cooldown'
                        self.text_manager.queue_text("Weapon Cooldown: -1", self.text_manager.BIG_FONT, {'center': (self.WIDTH/2, self.HEIGHT/2 + self.tile_size/2)}, 180)
                else:
                    if self.player.health < 10:
                        self.player.health += 1
                        "Buffed player health"
                        self.text_manager.queue_text("Player Health: +1", self.text_manager.BIG_FONT, {'center': (self.WIDTH/2, self.HEIGHT/2 + self.tile_size/2)}, 180)

            # not limiting the enemy buffs to make the game harder and challenging overtime
            if self.wave % 2 == 0 and self.upgraded == False:
                if chance == 1:
                    self.enemy_manager.damages.append(self.enemy_manager.damages[-1]+1) # add one damage
                    'enemy deals more damage'
                    self.text_manager.queue_text("Buffed monster attack damage", self.text_manager.BIG_FONT, {'center': (self.WIDTH/2, self.HEIGHT/2 - self.tile_size/2)}, 180)
                elif chance == 2:
                    self.enemy_manager.dash_speed.append(self.enemy_manager.dash_speed[-1]+1)
                    'enemy speed buffed'
                    self.text_manager.queue_text("Buffed monster speed", self.text_manager.BIG_FONT, {'center': (self.WIDTH/2, self.HEIGHT/2 - self.tile_size/2)}, 180)
                else:
                    self.enemy_manager.healths.append(self.enemy_manager.healths[-1]+1)
                    'enemy health buffed'
                    self.text_manager.queue_text("Buffed monster health", self.text_manager.BIG_FONT, {'center': (self.WIDTH/2, self.HEIGHT/2 - self.tile_size/2)}, 180)
                
                self.upgraded = True

    def spawn_wave(self):
        if len(self.enemy_manager.enemies) <= 0:
            if self.enemy_manager.can_spawn():
                self.enemy_spawn_rate = random.randint(5, 10) + self.enemy_spawn_rate
                self.spawn_enemies(self.enemy_spawn_rate)
                self.enemy_manager.spawn_cooldown_timer = self.enemy_manager.spawn_cooldown
                self.wave += 1
                self.upgraded = False
                self.text_manager.queue_text(f"Wave {self.wave}", self.text_manager.BIG_FONT, {'center': (self.WIDTH/2, self.HEIGHT/2)})

    def shoot(self, mx, my, mbutton, camera_offset):
        angle = math.degrees(math.atan2(my + camera_offset[1] - self.player.rect.centery, mx + camera_offset[0] - self.player.rect.centerx))
        if mbutton[0]:
            if self.weapon.shoot():
                self.sfx.play('shoot')
                self.bullet_manager.add_bullet(self.player.rect.center, angle + random.randint(-3, 3))

                self.player.ext_vel = vec2(-1, 0).rotate(angle).normalize() * 1 # knockback
                if abs(self.player.ext_vel.x) > abs(self.player.ext_vel.y):
                    self.player.scale(0.8, 1)
                else:
                    self.player.scale(1, 0.8)

    def update(self, delta_time):
        self.dt = delta_time
        mx, my = pygame.mouse.get_pos()
        mbutton = pygame.mouse.get_pressed()
                
        camera_offset = self.camera.offset(self.player, self.dt, mx, my)
        self.player.update(self.dt)
        
        if self.game_started and self.lost == False:
            self.shoot(mx, my, mbutton, camera_offset)

            # make all the enemies chase as soon as player moves or shoots
            if len(self.bullet_manager.bullets) > 0 or self.player.rect.topleft != self.player.ori_pos:
                self.enemy_manager.pursued = True

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
            self.bullet_manager.update(self.dt)
            self.tile_bullet_collision()
            self.entity_bullet_collision()

            self.upgrade()
            self.spawn_wave()

        self.draw(camera_offset)
        self.minimap()
        self.cursor.update(self.dt, self.window, (mx, my))
        
        # UI 
        # will only run once at the start of the program
        if self.game_started == False:
            if self.radius < self.WIDTH/2 + self.tile_size * 5:
                self.radius += 10 * self.dt
            else:
                self.game_started = True

        if self.lost:
            # fade in 
            if self.fade_in:
                if self.radius > 0:
                    self.radius -= 10 * self.dt
                else:
                    self.text_manager.queue_text("You Died", self.text_manager.BIG_FONT, {'center': (self.WIDTH/2, self.HEIGHT/2 - self.tile_size)}, None)
                    self.text_manager.queue_text("Press R to restart", self.text_manager.BIG_FONT, {'center': (self.WIDTH/2, self.HEIGHT/2 + self.tile_size)}, None)
                    self.text_manager.queue_text("Thank you for playing!", self.text_manager.SMALL_FONT, {'center': (self.WIDTH/2, self.HEIGHT - self.tile_size)}, None)

            # fade out
            else:
                if self.radius < self.WIDTH/2 + self.tile_size * 5:
                    self.radius += 10 * self.dt
                else:
                    self.lost = False

        if self.game_started == False or self.lost:      
            self.fade.fill((0, 0, 0))
            self.fade.set_colorkey((255, 255, 255))
            pygame.draw.circle(self.fade, (255, 255, 255), (self.WIDTH/2, self.HEIGHT/2), self.radius)
            self.window.blit(self.fade, (0, 0))

        self.text_manager.draw(self.window, self.dt)

    def event_controls(self, event):
        if event.type == pygame.KEYUP:
            self.player.keyup(event.key)

        if event.type == pygame.KEYDOWN:
            self.player.keydown(event.key)
            if self.text_manager.need_input:
                if event.key == pygame.K_r:
                    self.fade_in = False
                    self.text_manager.render_queue.clear()
                    self.restart()
