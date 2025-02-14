import noise, random
import math

def generate_world_data(world_size):
    tiles = {}
    center_x, center_y = world_size[0] // 2, world_size[1] // 2  # Center of the map
    max_distance = math.sqrt(center_x ** 2 + center_y ** 2)  # Max possible distance from center

    seed = random.randint(0, 10000)

    for y in range(world_size[1]):
        for x in range(world_size[0]):
            # Generate Perlin noise
            value = noise.pnoise2(x * 0.08, y * 0.08, octaves=1, persistence=0.5, base=256)

            # Calculate falloff factor (0 at center, 1 at edges)
            dx, dy = x - center_x, y - center_y
            distance = math.sqrt(dx**2 + dy**2)
            falloff = (distance / max_distance) ** 2  # Squared for smoother falloff

            # Apply falloff (reduces terrain values near edges)
            value -= falloff  

            # Determine terrain type
            terrain_type = 'air'
            if -0.15 < value <= 0.5:
                terrain_type = 'grass'
            elif -0.3 < value <= -0.15:
                terrain_type = 'dark grass'

            if terrain_type != 'air':
                tiles[(x, y)] = terrain_type
    
    return tiles
