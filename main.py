import asyncio
import pygame
from scripts.game import Game

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.init()
pygame.joystick.init()
# pygame.mixer.init()  # Initialize the mixer

window = pygame.display.set_mode((640, 360), pygame.SCALED|pygame.RESIZABLE)
pygame.display.set_caption('1 Blast')

game = Game(window)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

fps_event = pygame.USEREVENT
pygame.time.set_timer(fps_event, 250)
pygame.mouse.set_visible(0)


async def run(): 
    dt_setting = 60
    running = True

    while running:
        for event in pygame.event.get():
            game.event_controls(event)

            if event.type == pygame.QUIT:
                running = False
            
            if event.type == fps_event:
                pygame.display.set_caption(f"FPS: {clock.get_fps():.1f}")
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dt_setting = 5
                elif event.key == pygame.K_DOWN:
                    dt_setting = 60
            
        # Delta time 
        dt = clock.tick(1000) / 1000.0
        dt = min(dt, 1/20) 
        dt *= dt_setting

        # Update game
        window.fill((30, 30, 30))
        game.update(dt)

        pygame.display.flip()
        await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())

