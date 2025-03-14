#Resource handlers for the game

import pygame
import os

def load_png(name):
    fullname = os.path.join("graphics", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha():
            image = image.convert_alpha()
        else:
            image = image.convert()
    except pygame.error as msg:
        print("Could not load image", fullname)
        raise msg
    return image

class fake_sound: #A dummy sound object used if no sound is found
    def play(arg=0):
        pass

def load_sound(name):
    fullname = os.path.join("sound", name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as msg:
        print("Could not load sound", fullname)
        raise msg
        sound = fake_sound()
        return sound
    return sound
