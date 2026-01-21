import os

TILE_SIZE = 80
PLAYER_SIZE = 70
PLAYER_DISPLAY_SIZE = 140
SPEED = 5
COLLISION_TILES = ['W', 'B']

# Chemins
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
SPRITES_PATH = os.path.join(BASE_PATH, "sprites")

# Grille 4x3
WORLD_DATA = {
    (0,0): [
        "WWWWWWWWWWWWWWWWRGGGTTTG",
        "WWWWWWWWWWWWWWWWRRGGGTTG",
        "RRRWWWWWWWWWWWWWWWRGGGGG",
        "GGRWWWWWWWWWWRWWWWWRRRRR",
        "GGRRRWWWWWWWRRRWWWWWWWWW",
        "GGGGRRRWWWWRGGRRWWRRWWWW",
        "GGGGGGRRRRRRGGGRWBRRRRRR",
        "GTGGGPGGGGGGGGGRRBGGGGGG",
        "TTTGGGGGGGGGGRGGGGGGGTGG",
        "GGTGGGGGGGGGRRGGGGGGTTTG",
        "GGGGGGGTGGGGRRRGGGGGGTTG",
        "EGGGGGTTTGGGGRGGGGGGGGGG",
        "GGGGGGTTGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGEGGGGGGGGGGGG",
    ], # Map 1

    (1,0): [
        "WWWWWWWWWWWWWWWWWWWWWWWW",
        "                        ",
        "                        ",
        "                        ",
        "          P             ",
        "                        ",
        "W                       ",
        "W                       ",
        "W                       ",
        "W                       ",
        "                        ",
        "                        ",
        "                        ",
        "                        ",
    ], # Map 2

    (2,0): ["WWWW...", "..."], # Map 3
    (3,0): ["WWWW...", "..."], # Map 4
    (0,1): ["WWWW...", "..."], # Map 5 (en dessous de la 1)
    # ... remplissez jusqu'à (3,2)
}

# Format : (map_x, map_y): [(x, y, "nom_sprite", "message")]
INTERACTABLES_DATA = {
    (0, 0): [
        (400, 400, "chest.png", "Vous ouvrez le coffre de la Map 1 !")
    ],
    (3, 0): [
        (100, 500, "sign.png", "Panneau de la Map 4 : Bienvenue au bout du monde.")
    ],
    (1, 1): [
        (200, 200, "lever.png", "Un levier caché en Map 6.")
    ]
}

# Dimensions de l'écran (doivent être fixes pour détecter la sortie)
SCREEN_WIDTH = 24 * TILE_SIZE # Nb de caractères * TILE_SIZE
SCREEN_HEIGHT = 14 * TILE_SIZE