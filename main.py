import pygame as py
import asyncio
from scripts.game import Game

py.init()

window = py.display.set_mode([640, 360], py.SCALED)
py.display.set_caption('1 Blast')

game = Game(window)
clock = py.time.Clock()
font = py.font.Font(None, 32)

dt_setting = 60
fps_event = py.USEREVENT
py.time.set_timer(fps_event, 250)
py.mouse.set_visible(0)


async def run():
    running = True

    while running:
        for event in py.event.get():
            game.event_controls(event)

            if event.type == py.QUIT:
                running = False

        # Delta time 
        dt = clock.tick(1000) / 1000.0
        dt *= dt_setting
        dt = min(dt, 3) 

        # Update game
        window.fill((30, 30, 30))
        game.update(dt)

        py.display.flip()
        await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(run())
    # py.quit()
