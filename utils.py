import pygame
import os
from settings import SPRITES_PATH
import json

def load_img(name, size):
    path = os.path.join(SPRITES_PATH, name)
    if not os.path.exists(path):
        surf = pygame.Surface((size, size))
        surf.fill((255, 0, 255))
        return surf
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (size, size))


def load_tiles_config(file_path, tile_size):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    config = {}
    for entry in data:
        # Get the file name from the JSON path (ex: "water.png")
        sprite_name = os.path.basename(entry["sprite"])
        config[entry["id"]] = {
            "image": load_img(sprite_name, tile_size),
            "collision": entry["hasCollision"]
        }
    return config