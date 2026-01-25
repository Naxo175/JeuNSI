import os

TILE_SIZE = 80
PLAYER_DISPLAY_SIZE = 140
PLAYER_INTERACTION_AREA_SIZE = 20
SPEED = 10 # = 5

# File pathes
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
SPRITES_PATH = os.path.join(BASE_PATH, "sprites")

# Maps
MAPS_DATA = {
    (0, 0): [
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass","bush_tl"],["grass","barrier"],["grass","bush_tc"],["grass","bush_tc"],["grass","bush_tr"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass","bush_ml"],["grass"],["grass"],["grass"],["grass","bush_mr"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass","bush"],["grass"],["grass","bush_mr"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass","bush_ml"],["grass"],["grass"],["grass"],["grass","bush_mr"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass","bush_bl"],["grass","bush_bc"],["grass","bush_bc"],["grass","bush_bc"],["grass","bush_br"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass","trunk_left"],["water","trunk_center"],["water","trunk_center"],["water","trunk_center"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"]],
[["water"],["water"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["grass"],["water"],["water"],["water"]],
[["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"],["water"]]
    ],

    (1, 0): [
        # ...
    ]
}

# Interactables
INTERACTABLES_DATA = {
    # Format : (map_x, map_y): [(x, y, "id", "sprite.png", "name", "description")]
    (0, 0): [
        [500, 500, "ours_brun", "bear.png", "Bear", "It's a bear"],
        [500, 500, "mesange_nonnette", "bird1.png", "Bird1", "It's a bird n°1"],
        [500, 500, "mesange_charbonniere", "bird2.png", "Bird2", "It's a bird n°2"],
        [500, 500, "mesange_bleue", "bird3.png", "Bird3", "It's a bird n°3"],
        [500, 500, "mesange_a_longue_queue", "bird4.png", "Bird4", "It's a bird n°4"],
        [500, 500, "sanglier", "boar.png", "Boar", "It's a boar"],
        [500, 500, "cerf_elaphe", "deer.png", "Deer", "It's a deer"],
        [400, 400, "renard_roux", "fox.png", "Fox", "It's a fox"],
        [500, 500, "lapin_de_garenne", "rabbit.png", "Rabbit", "It's a rabbit"],
        [500, 500, "loup_gris", "wolf.png", "Wolf", "It's a wolf"],
    ],
    (1, 0): [
    ]
}

# Screen dimensions
SCREEN_WIDTH = 24 * TILE_SIZE # Map size X * TILE_SIZE
SCREEN_HEIGHT = 14 * TILE_SIZE # Map size Y * TILE_SIZE