from scripts.entities.entity import Entity

from scripts.utils import get_offset

class Enemy(Entity):
    def __init__(self, tile_size, pos):
        super().__init__(tile_size, pos)
        
        self.image.fill('#dfd8cd')

        self.flicker_timer = 0

        self.pursued = False
        self.purse_range = self.tile_size * 7
        self.speed = 1.4

        self.health = 3
    
    def draw(self, draw_surf, camera_offset):
        img = self.image.copy()
        if self.flicker_timer > 0 and int(self.flicker_timer) % 5 == 0:
            img.fill('red')
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]

        draw_surf.blit(img, (render_x, render_y))
    
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
            self.pursued = True
    
    def chase(self, entity):
        dx = entity.x - self.rect.x
        dy = entity.y - self.rect.y

        self.vel.x = dx
        self.vel.y = dy

    def update(self, delta_time, player):
        super().update(delta_time)

        self.pursue_target(player)
        if self.pursued:
            self.chase(player)

        if self.flicker_timer > 0:
            self.flicker_timer -= self.dt


class EnemyManager:
    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.enemies = []

    def spawn(self, pos):
        self.enemies.append(Enemy(self.tile_size, pos))
    
    def draw(self, draw_surf, camera_offset):
        for enemy in self.enemies:
            enemy.draw(draw_surf, camera_offset)

    def update(self, delta_time, player, ground_tiles, tiles):
        for enemy in self.enemies:
            enemy.update(delta_time, player)

            enemy_offset = get_offset(enemy, self.tile_size)
            collide_tiles = []
            for offset in [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
                tile_offset = (enemy_offset[0] + offset[0], enemy_offset[1] + offset[1])
                if tile_offset in ground_tiles:
                    collide_tiles.append(ground_tiles[tile_offset]) if ground_tiles[tile_offset].tile_type in ['air', 'edge'] else None
                if tile_offset in tiles:
                    collide_tiles.append(tiles[tile_offset]) if tiles[tile_offset].tile_type not in ['air', 'edge'] else None
            
            enemy.move(collide_tiles)

