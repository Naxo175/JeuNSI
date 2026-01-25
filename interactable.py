from utils import load_img
from settings import TILE_SIZE

class Interactable:
    def __init__(self, x, y, id, sprite, name, description):
        self.image = load_img(sprite, TILE_SIZE)
        self.id = id
        self.rect = self.image.get_rect(topleft=(x, y))
        self.name = name
        self.description = description

    def draw(self, screen):
        screen.blit(self.image, self.rect)