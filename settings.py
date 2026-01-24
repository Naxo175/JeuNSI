import os

TILE_SIZE = 80
PLAYER_DISPLAY_SIZE = 140
PLAYER_INTERACTION_AREA_SIZE = 20
SPEED = 10 # = 5

# File pathes
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
SPRITES_PATH = os.path.join(BASE_PATH, "sprites")

# Maps
WORLD_DATA = {
    (0,0): [
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water","water_rock2"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass","trunk_left"],["water","trunk_center"],["water","trunk_center"],["water","trunk_center"],["water","trunk_center"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water","water_rock3"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]]
    ],

    (1, 0): [
        # ...
    ]
}

# Format : (map_x, map_y): [(x, y, "sprite.png", "message")]
INTERACTABLES_DATA = {
    (0, 0): [
        (400, 400, "fox", "fox_idle.png", "Fox", "It's a fox")
    ],
    (3, 0): [
        (100, 500, "a", "aaaa.png", "AAAAAA", "aaa...")
    ],
    (1, 1): [
        (200, 200, "b", "bbbb.png", "bBbBb", "b...!!")
    ]
}

# Screen dimensions
SCREEN_WIDTH = 24 * TILE_SIZE # Map size X * TILE_SIZE
SCREEN_HEIGHT = 14 * TILE_SIZE # Map size Y * TILE_SIZE