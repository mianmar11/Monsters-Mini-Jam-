import random, math
import pygame

vec2 = pygame.math.Vector2

class Camera:
    def __init__(self, game_surf_size:tuple|list, tile_size):
        self.size = game_surf_size
        self.tile_size = tile_size

        self.gap = [0, 0]
        self.gap_size = self.tile_size * 3

        self.scroll = [0, 0]
        self.camera_speed = 10

        self.do_shake = False
        self.shake_timer = 0
        self.shake_dur = 6
        self.shake_offset = [0, 0]

        # motion
        self.doing_cam_transition = False
        self.transition_direction = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
    
    def start_shake(self, intensity):
        self.do_shake = True
        self.shake_timer = self.shake_dur

        self.shake_offset[0] = random.choice([-intensity, intensity])
        self.shake_offset[1] = random.choice([-intensity, intensity])

    def shake(self):
        self.shake_timer -= self.dt
        if self.shake_timer < 0:
            self.do_shake = False
            self.shake_offset = [0, 0]
        
        self.shake_offset[0] += (0 - self.shake_offset[0]) * 0.5 * self.dt
        self.shake_offset[1] += (0 - self.shake_offset[1]) * 0.5 * self.dt

    def offset(self, player, delta_time, mx, my):
        self.dt = delta_time

        angle = math.degrees(math.atan2(my + self.scroll[1] - player.rect.centery, mx + self.scroll[0] - player.rect.centerx))
        gap = [math.cos(math.radians(angle)) * self.gap_size, math.sin(math.radians(angle)) * self.gap_size]

        self.gap[0] += (gap[0] - self.gap[0]) * 0.1 * self.dt
        self.gap[1] += (gap[1] - self.gap[1]) * 0.1 * self.dt

        self.scroll[0] += (player.rect.centerx - self.scroll[0] - self.size[0] / 2) * 0.8 * self.dt 
        self.scroll[1] += (player.rect.centery - self.scroll[1] - self.size[1] / 2) * 0.8 * self.dt

        if self.do_shake:
            self.shake()

        return int(self.scroll[0] + self.shake_offset[0] + self.gap[0]), int(self.scroll[1] + self.shake_offset[1] + self.gap[1])
    