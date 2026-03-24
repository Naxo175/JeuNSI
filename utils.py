import pygame
import os
import sys
from settings import SPRITES_PATH
import json

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_img(name, size):
    raw_path = os.path.join(SPRITES_PATH, name)
    path = resource_path(raw_path)
    
    if not os.path.exists(path):
        surf = pygame.Surface((size, size))
        surf.fill((255, 0, 255))
        return surf
        
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (size, size))


def load_tiles_config(file_path, tile_size):
    path_to_json = resource_path(file_path)
    
    with open(path_to_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    config = {}
    for entry in data:
        sprite_name = os.path.basename(entry["sprite"])
        
        config[entry["id"]] = {
            "image": load_img(sprite_name, tile_size),
            "collision": entry["hasCollision"]
        }
    
    return config