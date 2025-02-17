import pygame

class TextManager:
    def __init__(self, tile_size, window_size):
        self.tile_size = tile_size
        self.WIDTH, self.HEIGHT = window_size
        self.BIG_FONT = pygame.font.Font(None, self.tile_size * 2)
        self.SMALL_FONT = pygame.font.Font(None, self.tile_size)

        # Store default text data
        self.text_data = {
            "You died": (self.BIG_FONT, {"center": (self.WIDTH / 2, self.HEIGHT / 2)}),
            "Press R to play again": (self.BIG_FONT, {"center": (self.WIDTH / 2, self.HEIGHT / 2 + self.tile_size)}),
            "Thank you for playing": (self.SMALL_FONT, {"bottom": (self.WIDTH / 2, self.HEIGHT - self.tile_size / 2)}),
        }

        self.render_queue = []  # Stores texts that need to be drawn

        self.cooldown = 60

        self.need_input = False

    def queue_text(self, text, font=None, pos=None, cooldown=60):
        """
        Adds text to the render queue.
        - `text`: The string to render
        - `font`: pygame Font object (defaults to BIG_FONT)
        - `pos`: Dictionary with rect positioning (e.g., {"center": (x, y)})
        """
        if font is None:
            font = self.BIG_FONT  # Default to big font
        if pos is None:
            pos = {"topleft": (10, 10)}  # Default position

        self.render_queue.append([text, font, pos, cooldown])

    def draw(self, draw_surf, dt):
        """
        Draws all texts from the render queue onto the screen.
        """
        self.need_input = False
        
        for item in self.render_queue.copy():
            text, font, pos, cooldown = item
            img = font.render(text, False, "white")
            rect = img.get_rect(**pos)
            draw_surf.blit(img, rect)

            if item[-1] != None:
                item[-1] -= dt
                if item[-1] < 0:
                    self.render_queue.remove(item)  # Clear queue after rendering
            else:
                self.need_input = True
        
        return self.need_input
