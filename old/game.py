import pygame
import math
import os

# Initialisation
pygame.init()

# Mode plein écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

TILE_SIZE = 40
PLAYER_SIZE = 35

# Chemin absolu
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def load_img(name, size):
    path = os.path.join(BASE_PATH, "sprites", name)
    if not os.path.exists(path):
        surf = pygame.Surface((size, size))
        surf.fill((255, 0, 255))
        return surf
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (size, size))

# --- CONFIGURATION DU JEU ---

# 1. Ajoutez ici les caractères qui doivent bloquer le joueur
COLLISION_TILES = ['W', 'B'] 

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

tile_images = {
    'W': load_img("wall.png", TILE_SIZE),
    'G': load_img("grass.png", TILE_SIZE),
    'D': load_img("dirt.png", TILE_SIZE),
    'B': load_img("wood.png", TILE_SIZE),
}

player_sprites = {
    (0, -1):  load_img("player_up.png", PLAYER_SIZE),
    (0, 1):   load_img("player_down.png", PLAYER_SIZE),
    (-1, 0):  load_img("player_left.png", PLAYER_SIZE),
    (1, 0):   load_img("player_right.png", PLAYER_SIZE),
    (-1, -1): load_img("player_up_left.png", PLAYER_SIZE),
    (1, -1):  load_img("player_up_right.png", PLAYER_SIZE),
    (-1, 1):  load_img("player_down_left.png", PLAYER_SIZE),
    (1, 1):   load_img("player_down_right.png", PLAYER_SIZE),
    (0, 0):   load_img("player_idle.png", PLAYER_SIZE),
}

# --- GÉNÉRATION DU NIVEAU ---
walls = []
floor_tiles = []
player_x, player_y = 0, 0
current_dir = (0, 1)

for r, row in enumerate(MAP_DATA):
    for c, char in enumerate(row):
        x, y = c * TILE_SIZE, r * TILE_SIZE
        
        # Position de départ
        if char == 'P':
            player_x, player_y = x, y
            char = 'G' # On met de l'herbe sous le joueur au spawn
        
        # Choix de la texture
        tile_char = char if char in tile_images else 'G'
        floor_tiles.append((tile_images[tile_char], (x, y)))
        
        # --- GESTION DYNAMIQUE DES COLLISIONS ---
        if char in COLLISION_TILES:
            walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
speed = 5

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT] or keys[pygame.K_q]:  dx = -1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1
    if keys[pygame.K_UP] or keys[pygame.K_z]:    dy = -1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:  dy = 1

    if dx != 0 or dy != 0:
        current_dir = (dx, dy)
        length = math.sqrt(dx**2 + dy**2)
        dx, dy = dx/length, dy/length

    # Mouvement X
    player_x += dx * speed
    player_rect.x = int(player_x)
    for wall in walls:
        if player_rect.colliderect(wall):
            player_x -= dx * speed
            player_rect.x = int(player_x)

    # Mouvement Y
    player_y += dy * speed
    player_rect.y = int(player_y)
    for wall in walls:
        if player_rect.colliderect(wall):
            player_y -= dy * speed
            player_rect.y = int(player_y)

    # Rendu
    screen.fill((0, 0, 0))
    for img, pos in floor_tiles:
        screen.blit(img, pos)

    sprite_to_draw = player_sprites.get(current_dir, player_sprites[(0, 0)])
    screen.blit(sprite_to_draw, (player_rect.x, player_rect.y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()