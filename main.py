import pygame
from settings import *
from utils import load_img
from player import Player
from interactable import Interactable

pygame.init()
# On utilise les dimensions calculées dans settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Coordonnées actuelles dans le monde (on commence à la Map 1 en haut à gauche)
current_map_pos = [0, 0]

def load_map(map_coords):
    """Génère les objets de la map spécifiée"""
    new_walls = []
    new_floor = []
    spawn_pos = None
    
    data = WORLD_DATA.get(tuple(map_coords), WORLD_DATA[(0,0)])
    
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            x, y = c * TILE_SIZE, r * TILE_SIZE
            if char == 'P':
                spawn_pos = (x, y)
                char = 'G'
            
            tile_char = char if char in tile_images else 'G'
            new_floor.append((tile_images[tile_char], (x, y)))
            
            if char in COLLISION_TILES:
                new_walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    
    # Charger les objets de cette map
    new_interactables = []
    objs = INTERACTABLES_DATA.get(tuple(map_coords), [])
    for x, y, sprite, msg in objs:
        new_interactables.append(Interactable(x, y, sprite, msg))
        
    return new_floor, new_walls, spawn_pos, new_interactables

# Initialisation du premier niveau
tile_images = {
    'W': load_img("water.png", TILE_SIZE),
    'G': load_img("grass.png", TILE_SIZE),
    'D': load_img("dirt.png", TILE_SIZE),
    'R': load_img("water_rock1.png", TILE_SIZE),
    'S': load_img("water_rock2.png", TILE_SIZE),
    'T': load_img("water_rock3.png", TILE_SIZE),
}

floor_tiles, walls, player_spawn, interactables = load_map(current_map_pos)
player = Player(player_spawn[0], player_spawn[1])

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_e:
                player.check_interaction(interactables)

    # 1. Gestion des entrées et Update
    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] or keys[pygame.K_d] - keys[pygame.K_q]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP] or keys[pygame.K_s] - keys[pygame.K_z]
    player.move(dx, dy, walls)

    # 2. Détection de sortie d'écran (Transition)
    transition = False
    
    # Sortie à DROITE
    if player.rect.left > SCREEN_WIDTH:
        current_map_pos[0] += 1
        player.pos.x = -PLAYER_SIZE # Réapparaît à gauche
        transition = True
    # Sortie à GAUCHE
    elif player.rect.right < 0:
        current_map_pos[0] -= 1
        player.pos.x = SCREEN_WIDTH # Réapparaît à droite
        transition = True
    # Sortie en BAS
    elif player.rect.top > SCREEN_HEIGHT:
        current_map_pos[1] += 1
        player.pos.y = -PLAYER_SIZE # Réapparaît en haut
        transition = True
    # Sortie en HAUT
    elif player.rect.bottom < 0:
        current_map_pos[1] -= 1
        player.pos.y = SCREEN_HEIGHT # Réapparaît en bas
        transition = True

    # 3. Recharger la map si besoin
    if transition:
        # On sauvegarde les anciennes coordonnées pour vérifier si on a bougé
        old_map_pos = list(current_map_pos)
        
        current_map_pos[0] = max(0, min(3, current_map_pos[0]))
        current_map_pos[1] = max(0, min(2, current_map_pos[1]))
        
        # MISE À JOUR ICI : On récupère les 4 valeurs, dont les nouveaux interactables
        floor_tiles, walls, _, interactables = load_map(current_map_pos)
        
        player.rect.topleft = (int(player.pos.x), int(player.pos.y))

    # 4. Dessin
    screen.fill((0, 0, 0))
    for img, pos in floor_tiles:
        screen.blit(img, pos)
    
    if(player):
        player.draw(screen)
    
    for obj in interactables:
        obj.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()