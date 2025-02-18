import pygame, random

class SFX:
    def __init__(self):
        pygame.mixer.init()  # Initialize the mixer
        self.sounds = {
            "shoot": [pygame.mixer.Sound("sfx/shoot.wav"), pygame.mixer.Sound("sfx/shoot2.wav")],
            'hit': [pygame.mixer.Sound("sfx/hit.wav"), pygame.mixer.Sound("sfx/hit2.wav")],
            "music": [pygame.mixer.Sound("sfx/beat3.wav")]
        }

    def play(self, sound_name, volume=1, loop=0):
        random.choice(self.sounds[sound_name]).play(loop)
        self.set_volume(sound_name, volume)

    def set_volume(self, sound_name, volume):
        [sound.set_volume(volume) for sound in self.sounds[sound_name]]

    def stop(self, sound_name):
        self.sounds[sound_name].stop()

    def stop_all(self):
        for sound in self.sounds.values():
            sound.stop()
