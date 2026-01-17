import pygame
import math
import os

# Initialisation
pygame.init()

TILE_SIZE = 40
PLAYER_SIZE = 35

# Fonction utilitaire pour charger et redimensionner proprement
def load_img(name, size):
    path = os.path.join("sprites", name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (size, size))
    except:
        # Si l'image manque, on crée un carré de couleur par défaut
        surf = pygame.Surface((size, size))
        surf.fill((255, 0, 255)) # Rose "erreur"
        return surf

# --- CONFIGURATION DE LA CARTE ---
MAP_DATA = [
    "WWWWWWWWWWWWWWWWWWWW",
    "WGGGGGGGGGGGGGGGGGGW",
    "WG  P             GW",
    "WGGGG    BBBB     GW",
    "WDDDD    B  B     GW",
    "WDDDD    BBBB     GW",
    "WWWWWWWWWWWWWWWWWWWW",
]

# --- CHARGEMENT DES TILES ---
tile_images = {
    'W': load_img("wall.png", TILE_SIZE),
    'G': load_img("grass.png", TILE_SIZE),
    'D': load_img("dirt.png", TILE_SIZE),
    'B': load_img("wood.png", TILE_SIZE),
}

# --- CHARGEMENT DU JOUEUR ---
# On mappe les directions (dx, dy) aux noms de fichiers
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
WIDTH = len(MAP_DATA[0]) * TILE_SIZE
HEIGHT = len(MAP_DATA) * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

walls = []
floor_tiles = []
player_x, player_y = 0, 0
current_dir = (0, 1)

for r, row in enumerate(MAP_DATA):
    for c, char in enumerate(row):
        x, y = c * TILE_SIZE, r * TILE_SIZE
        if char == 'P':
            player_x, player_y = x, y
        
        # On remplit toujours le sol par de l'herbe par défaut si c'est vide
        # ou on dessine la tuile spécifiée
        tile_char = char if char in tile_images else 'G'
        floor_tiles.append((tile_images[tile_char], (x, y)))
        
        if char in ['W', 'B']:
            walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
speed = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

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

    # Mouvement et collisions
    player_x += dx * speed
    player_rect.x = int(player_x)
    for wall in walls:
        if player_rect.colliderect(wall):
            player_x -= dx * speed
            player_rect.x = int(player_x)

    player_y += dy * speed
    player_rect.y = int(player_y)
    for wall in walls:
        if player_rect.colliderect(wall):
            player_y -= dy * speed
            player_rect.y = int(player_y)

    # Affichage
    for img, pos in floor_tiles:
        screen.blit(img, pos)

    sprite_to_draw = player_sprites.get(current_dir, player_sprites[(0, 0)])
    screen.blit(sprite_to_draw, (player_rect.x, player_rect.y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()