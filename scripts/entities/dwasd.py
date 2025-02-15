import pygame 

pygame.init(
)

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

tile_size = 64
AUTOTILE_MAP = {
        # rects which will render on the image so that they will show the edge highlights
        tuple(sorted([(0, 1), (1, 0)])): [(0, 0, tile_size, tile_size/8), (0, 0, tile_size/8, tile_size)], # topleft
        tuple(sorted([(0, 1), (1, 0), (-1, 0)])): [(0, 0, tile_size, tile_size/8)], # middletop
        tuple(sorted([(0, 1), (-1, 0)])): [(0, 0, tile_size, tile_size/8), (tile_size - tile_size/8, 0, tile_size/8, tile_size)], # topright

        tuple(sorted([(0, -1), (1, 0), (0, 1)])): [(0, 0, tile_size/8, tile_size)], # left
        tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0)])): [], # middle
        tuple(sorted([(0, 1), (-1, 0), (0, -1)])): [(tile_size - tile_size/8, 0, tile_size/8, tile_size)], # right

        tuple(sorted([(0, -1), (1, 0)])): [(0, tile_size - tile_size/8, tile_size, tile_size/8), (0, 0, tile_size/8, tile_size)], # bottomleft
        tuple(sorted([(0, -1), (-1, 0), (1, 0)])): [(0, tile_size - tile_size/8, tile_size, tile_size/8)], # bottom
        tuple(sorted([(0, -1), (-1, 0)])): [(0, tile_size - tile_size/8, tile_size, tile_size/8), (tile_size - tile_size/8, 0, tile_size/8, tile_size)], # bottomright
    }

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    screen.fill((0, 0, 0))

    for i, rects in enumerate(AUTOTILE_MAP.values()):
        x = i % 3
        y = i // 3
        print(i, (x, y))
        for rect in rects:
            pygame.draw.rect(screen, 'white', (rect[0] + x * tile_size, rect[1] + y * tile_size, rect[2], rect[3]))

    pygame.display.flip()
    clock.tick(60)