import os

TILE_SIZE = 40
PLAYER_SIZE = 35
PLAYER_DISPLAY_SIZE = 70
SPEED = 5
COLLISION_TILES = ['W', 'B']

# Chemins
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
SPRITES_PATH = os.path.join(BASE_PATH, "sprites")

MAP_DATA = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                              W",
    "W                                              W",
    "W         WWWW                                 W",
    "W   WW                                         W",
    "W   WW        W                                W",
    "W             W                                W",
    "WWWWWWWWWWWWWWW WWWWW  BBB                     W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W         P                                    W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "W                                              W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]