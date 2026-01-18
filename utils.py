import pygame
import os
from settings import SPRITES_PATH

def load_img(name, size):
    path = os.path.join(SPRITES_PATH, name)
    if not os.path.exists(path):
        surf = pygame.Surface((size, size))
        surf.fill((255, 0, 255))
        return surf
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (size, size))