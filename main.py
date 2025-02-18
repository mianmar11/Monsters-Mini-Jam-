import pygame
import asyncio
from scripts.game import Game

pygame.init()

window = pygame.display.set_mode([640, 360], pygame.SCALED)
pygame.display.set_caption('1 Blast')

game = Game(window)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

dt_setting = 60
fps_event = pygame.USEREVENT
pygame.time.set_timer(fps_event, 250)
pygame.mouse.set_visible(0)


async def run():
    running = True

    while running:
        for event in pygame.event.get():
            game.event_controls(event)

            if event.type == pygame.QUIT:
                running = False
            
            if event.type == fps_event:
                pygame.display.set_caption(f"FPS: {clock.get_fps():.1f}")

        # Delta time 
        dt = clock.tick(1000) / 1000.0
        dt *= dt_setting
        dt = min(dt, 3) 

        # Update game
        window.fill((30, 30, 30))
        game.update(dt)

        pygame.display.flip()
        await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(run())
    # pygame.quit()
