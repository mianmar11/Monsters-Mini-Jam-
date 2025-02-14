import noise, random
import math

def generate_world_data(world_size):
    tiles = {}
    center_x, center_y = world_size[0] // 2, world_size[1] // 2  # Center of the map
    max_distance = math.sqrt(center_x ** 2 + center_y ** 2)  # Max possible distance from center

    seed = random.randint(0, 256)

    for y in range(world_size[1]):
        for x in range(world_size[0]):
            # Generate Perlin noise
            value = noise.pnoise2(x * 0.05, y * 0.08, octaves=2, persistence=0.5, base=seed)

            # Calculate falloff factor (0 at center, 1 at edges)
            dx, dy = x - center_x, y - center_y
            distance = math.sqrt(dx**2 + dy**2)
            t = distance / max_distance
            falloff = (1 - math.cos(t * math.pi)) * 0.58

            # Apply falloff (reduces terrain values near edges)
            value -= falloff  

            # Determine terrain type
            terrain_type = 'air'
            if -0.3 < value <= 1:
                terrain_type = 'dirt'
            elif -0.5 < value <= -0.3:
                terrain_type = 'dirt2'

            # if terrain_type != 'air':
            tiles[(x, y)] = terrain_type
    
    return tiles
