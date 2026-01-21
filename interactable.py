from utils import load_img
from settings import TILE_SIZE

class Interactable:
    def __init__(self, x, y, sprite_name, message):
        self.image = load_img(sprite_name, TILE_SIZE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.message = message

    def interact(self):
        # Pour l'instant un simple print, mais pourra déclencher n'importe quoi
        print(f"Interaction : {self.message}")

    def draw(self, screen):
        screen.blit(self.image, self.rect)