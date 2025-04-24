class RangeWeapon:
    def __init__(self, tile_size):
        self.tile_size = tile_size

        self.cooldown = 12
        self.cooldown_timer = 0

        self.rounds = 20
        self.reload_time = 120
        self.reload_timer = 0

        self.multishot = False
    
    def shoot(self):
        if self.cooldown_timer <= 0 and self.rounds > 0:
            self.cooldown_timer = self.cooldown
            
            self.rounds -= 1
            if self.rounds <= 0:
                self.reload_timer = self.reload_time
            
            return True
        return 

    def reloading(self):
        if self.reload_timer <= 0:
            return False
        return True

    def update(self, delta_time):
        self.dt = delta_time

        if self.cooldown_timer > 0:
            self.cooldown_timer -= self.dt
        
        if self.reload_timer > 0:
            self.reload_timer -= self.dt
            if self.reload_timer <= 0:
                self.rounds = 20
                self.reload_timer = 0