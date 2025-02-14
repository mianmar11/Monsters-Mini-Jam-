import pygame as py
import os   

from scripts.game import Game

class App:
    # initialize window 
    def __init__(self):
        py.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.aspect_ratio = (16, 9)
        self.window  = py.display.set_mode([640, 360], py.SCALED)
        self.mainClock = py.time.Clock()  
        self.font = py.font.Font(None, 32)  

        self.game = Game(self.window)
        
        self.running = True                  
        self.dt_setting = 60
        self.fps_event = py.USEREVENT
        self.fps = '0'
        py.time.set_timer(self.fps_event, 250)

    def run(self):
        while self.running:
            for event in py.event.get():
                self.game.event_controls(event)

                if event.type == py.QUIT:
                    self.running = False
                
                if event.type == self.fps_event:
                    self.fps = f"{self.mainClock.get_fps():.1f}"
                
                # if event.type == py.KEYDOWN:
                #     if event.key == py.K_F11:
                #         py.display.toggle_fullscreen()

            dt = self.mainClock.tick(1000) / 1000.0
            dt *= self.dt_setting
            if dt > 3: 
                dt = 3

            self.window.fill((0, 0, 0))
            self.game.update(dt)
            
            fps = self.font.render(f'FPS: {self.fps}', True, 'white')
            self.window.blit(fps, (10, 10))
 
            py.display.flip()
            if py.key.get_pressed()[py.K_UP]:
                self.dt_setting = 10
            if py.key.get_pressed()[py.K_DOWN]:
                self.dt_setting = 60
    
app = App()
    
if __name__ == '__main__':
    app.run()
    py.quit()