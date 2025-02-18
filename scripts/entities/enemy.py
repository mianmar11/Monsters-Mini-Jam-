import random, pygame

from scripts.entities.entity import Entity

from scripts.utilities.utils import get_offset

class Enemy(Entity):
    def __init__(self, tile_size, pos, damage=1, health=3, dash_speed=6):
        super().__init__(tile_size, pos)
        
        self.image.fill('#e9e3d9')

        self.pursued = False
        self.purse_range = self.tile_size * 7
        
        self.speed = 0
        self.dash_speed = dash_speed
        self.cooldown = 60

        self.health = health
        self.damage = damage

        self.process_timer = 24
        self.flicker_timer = 0
        self.dash_timer = 8
        self.dash_cooldown_timer = random.randint(0, self.cooldown)
    
    def bullet_collision(self, bullets):
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                self.health -= bullet.damage
                return True

    def pursue_target(self, entity):
        self.vel.x = 0
        self.vel.y = 0

        dx = entity.x - self.x
        dy = entity.y - self.y
        distance = (dx**2 + dy**2)**0.5

        if distance < self.purse_range:
            self.get_pursue()
    
    def get_pursue(self):
        self.pursued = True
        self.scale(0.5, 1.5)
    
    def chase(self, entity):
        dx = entity.x - self.rect.x
        dy = entity.y - self.rect.y

        self.dash_timer -= self.dt
        if self.dash_timer < 0:
            self.dash_cooldown_timer -= self.dt
            if self.dash_cooldown_timer < 0:
                angle = random.randint(1, 45)
                self.vel.x = dx
                self.vel.y = dy
                self.vel = self.vel.rotate(random.choice([0, angle, -angle]))
                self.dash_cooldown_timer = self.cooldown
                self.dash_timer = 6
                self.scale(0.6, 1.4)
                return

    def move(self, tiles):
        if self.vel.length() > 0:
            self.vel = self.vel.normalize()

        if self.dash_timer > 0:
            self.speed += (self.dash_speed - self.speed) * self.dt
        else:
            self.speed += (0 - self.speed) * 0.5 * self.dt
        self.total_vel = self.vel * self.speed + self.ext_vel

        self.y += self.total_vel.y * self.dt
        self.rect.y = self.y
        self.vertical_collision(tiles)
        self.rect.y = self.y

        self.x += self.total_vel.x * self.dt
        self.rect.x = self.x
        self.horizontal_collision(tiles)
        self.rect.x = self.x

    def update(self, delta_time, player):
        super().update(delta_time)

        if self.pursued == False:
            self.pursue_target(player)
        else:
            self.process_timer -= self.dt
            if self.process_timer < 0:
                self.chase(player)


class EnemyManager:
    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.enemies = []
        self.damages = [1]
        self.healths = [3]
        self.dash_speed = [6]
        self.pursued = False

        self.spawn_cooldown = 180
        self.spawn_cooldown_timer = 180

    def can_spawn(self):
        self.spawn_cooldown_timer -= self.dt
        if self.spawn_cooldown_timer < 0:
            return True
        return

    def spawn(self, pos):
        self.enemies.append(Enemy(self.tile_size, pos, random.choice(self.damages), random.choice(self.healths), random.choice(self.dash_speed)))
    
    def draw(self, draw_surf, camera_offset):
        for enemy in self.enemies:
            enemy.draw(draw_surf, camera_offset)

    def update(self, delta_time, player, ground_tiles, tiles):
        self.dt = delta_time
        for enemy in self.enemies:
            enemy.update(delta_time, player)

            enemy_offset = get_offset(enemy, [self.tile_size]*2)
            collide_tiles = []
            for offset in [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
                tile_offset = (enemy_offset[0] + offset[0], enemy_offset[1] + offset[1])
                if tile_offset in ground_tiles:
                    collide_tiles.append(ground_tiles[tile_offset]) if ground_tiles[tile_offset].tile_type in ['air', 'edge'] else None
                if tile_offset in tiles:
                    collide_tiles.append(tiles[tile_offset]) if tiles[tile_offset].tile_type not in ['air', 'edge'] else None
            
            enemy.move(collide_tiles)

            # make all the enemies pursued
            if enemy.pursued:
                self.pursued = True
            if self.pursued and enemy.pursued == False:
                enemy.get_pursue()

