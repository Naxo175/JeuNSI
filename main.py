import pygame
from settings import *
from utils import load_tiles_config
from player import Player
from interactable import Interactable
from inventory_ui import InventoryUI

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Initialisation du mixeur (si pas déjà fait via pygame.init())
pygame.mixer.init()

# Charger le fichier MP3
# Remplace 'musique.mp3' par ton chemin de fichier
try:
    pygame.mixer.music.load("audio/music.mp3")
    
    # Jouer la musique
    # -1 signifie que la musique boucle à l'infini
    pygame.mixer.music.play(loops=-1)
    
    # Optionnel : régler le volume (0.0 à 1.0)
    pygame.mixer.music.set_volume(1)
except pygame.error as e:
    print(f"Cannot load music : {e}")

TILE_CONFIG = load_tiles_config("tiles.json", TILE_SIZE)

def load_map(map_coords):
    walls = []
    tiles_below_player = []  # Layers <2
    tiles_above_player = []  # Layers >=2
    
    data = MAPS_DATA.get(tuple(map_coords), MAPS_DATA[(0, 0)])
    
    for r, row in enumerate(data):
        for c, tile_stack in enumerate(row):
            x, y = c * TILE_SIZE, r * TILE_SIZE
            highest_tile_info = None
            
            # On utilise l'index (i) pour connaître le Layer
            for i, tile_id in enumerate(tile_stack):
                if not tile_id:
                    continue
                
                tile_info = TILE_CONFIG.get(tile_id)
                if tile_info:
                    # Séparation selon l'index de la pile
                    if i < 2:
                        tiles_below_player.append((tile_info["image"], (x, y)))
                    else:
                        tiles_above_player.append((tile_info["image"], (x, y)))
                    
                    highest_tile_info = tile_info

            if highest_tile_info and highest_tile_info["collision"]:
                walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    
    # --- Chargement des interactibles ---
    interactables = []
    objs = INTERACTABLES_DATA.get(tuple(map_coords), [])
    for x, y, uid, sprite, name, description in objs:
        interactables.append(Interactable(x, y, uid, sprite, name, description))
    
    return tiles_below_player, tiles_above_player, walls, interactables

# Spawn configuration
START_MAP = [0, 0]
START_X = 2 * TILE_SIZE
START_Y = 13 * TILE_SIZE

current_map_pos = START_MAP

# Load start map
tiles_below_player, tiles_above_player, walls, interactables = load_map(current_map_pos)

# Create the Player at start coordinates
player = Player(START_X, START_Y)

# UI
inventory_ui = InventoryUI()

running = True
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_e:
                collected_item = player.check_interaction(interactables)
            if event.key == pygame.K_a:
                inventory_ui.toggle()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
            if inventory_ui.is_open:
                inventory_ui.handle_click(event.pos, player.inventory)



    # Inputs and Movement
    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    if not inventory_ui.is_open:
        player.move(dx, dy, walls)



    # Screen exit detection (Transition)
    transition = False
    
    # Exit to Right -> respawns to Left
    if player.rect.left > SCREEN_WIDTH:
        current_map_pos[0] += 1
        player.pos.x = -5
        transition = True
    # Exit to Left -> respawns to Right
    elif player.rect.right < 0:
        current_map_pos[0] -= 1
        player.pos.x = SCREEN_WIDTH-5
        transition = True
    # Exit to Down -> respawns to Up
    elif player.rect.top > SCREEN_HEIGHT:
        current_map_pos[1] += 1
        player.pos.y = -5
        transition = True
    # Exit to Up -> respawns to Down
    elif player.rect.bottom < 0:
        current_map_pos[1] -= 1
        player.pos.y = SCREEN_HEIGHT-5
        transition = True


    if transition:
        current_map_pos[0] = max(0, min(3, current_map_pos[0]))
        current_map_pos[1] = max(0, min(2, current_map_pos[1]))

        tiles_below_player, tiles_above_player, walls, interactables = load_map(current_map_pos)
        
        player.rect.topleft = (int(player.pos.x), int(player.pos.y))



    # Draw the game
    screen.fill((0, 0, 0))

    for img, pos in tiles_below_player:
        screen.blit(img, pos)

    for obj in interactables:
        obj.draw(screen)
    
    if(player):
        player.draw(screen)
    
    for img, pos in tiles_above_player:
        screen.blit(img, pos)

    inventory_ui.draw(screen, player.inventory)


    # DEBUG
    # for wall in walls:
    #     pygame.draw.rect(screen, (255, 0, 0), wall, 1)
    
    pygame.display.flip()
    clock.tick(60)


pygame.quit()