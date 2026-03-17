import pygame
from settings import *
from utils import load_tiles_config
from player import Player
from interactable import Interactable
from inventory_ui import InventoryUI

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.mixer.init() # Initialise le système audio

try:
    pygame.mixer.music.load("audio/music.ogg") # Charge le fichier audio
    pygame.mixer.music.play(loops=-1) # Lance la lecture en boucle
    pygame.mixer.music.set_volume(1) # Règle le volume
except pygame.error as e:
    print(f"Cannot load music : {e}")

TILE_CONFIG = load_tiles_config("tiles.json", TILE_SIZE) # Charge les données des Tiles

def load_map(map_coords):
    walls = []
    tiles_below_player = []  
    tiles_above_player = []  
    
    data = MAPS_DATA.get(tuple(map_coords), MAPS_DATA[(0, 1)]) # Récupère les données de la carte
    
    for r, row in enumerate(data):
        for c, tile_stack in enumerate(row):
            x, y = c * TILE_SIZE, r * TILE_SIZE # Calcule la position en pixels
            highest_tile_info = None
            
            for i, tile_id in enumerate(tile_stack):
                if not tile_id:
                    continue
                
                tile_info = TILE_CONFIG.get(tile_id)
                if tile_info:
                    if i < 2: # Assigne aux couches inférieures
                        tiles_below_player.append((tile_info["image"], (x, y)))
                    else: # Assigne aux couches supérieures
                        tiles_above_player.append((tile_info["image"], (x, y)))
                    
                    highest_tile_info = tile_info

            if highest_tile_info and highest_tile_info["collision"]: # Si la Tile la plus haute de cette case a de la collision
                walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)) # On la met dans la liste "walls"
    
    interactables = []
    objs = INTERACTABLES_DATA.get(tuple(map_coords), [])
    for x, y, uid, sprite, name in objs: # Instancie les objets de la map
        interactables.append(Interactable(x, y, uid, sprite, name))
    
    return tiles_below_player, tiles_above_player, walls, interactables

START_MAP = [0, 1]
START_X = 5 * TILE_SIZE
START_Y = 4 * TILE_SIZE

current_map_pos = START_MAP

tiles_below_player, tiles_above_player, walls, interactables = load_map(current_map_pos) # Initialise l'environnement

player = Player(START_X, START_Y) # Initialise le joueur
inventory_ui = InventoryUI() # Initialise l'interface utilisateur

running = True
while running:

    for event in pygame.event.get(): # Boucle des événements
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_e: # Déclenche la détection d'interaction
                collected_item = player.check_interaction(interactables)
            if event.key == pygame.K_a: # Alterne l'état de l'affichage UI
                inventory_ui.toggle()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if inventory_ui.is_open: # Transmet les coordonnées du clic à l'UI
                inventory_ui.handle_click(event.pos, player.inventory)

    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    if not inventory_ui.is_open: # Bloque le mouvement si l'inventaire est ouvert
        player.move(dx, dy, walls)

    transition = False # Variable booléenne pour le changement de map
    
    if player.rect.left > SCREEN_WIDTH:
        current_map_pos[0] += 1
        player.pos.x = -5
        transition = True
    elif player.rect.right < 0:
        current_map_pos[0] -= 1
        player.pos.x = SCREEN_WIDTH-5
        transition = True
    elif player.rect.top > SCREEN_HEIGHT:
        current_map_pos[1] += 1
        player.pos.y = -5
        transition = True
    elif player.rect.bottom < 0:
        current_map_pos[1] -= 1
        player.pos.y = SCREEN_HEIGHT-5
        transition = True

    if transition: # Actualise les données lors du changement de map
        current_map_pos[0] = max(0, min(3, current_map_pos[0]))
        current_map_pos[1] = max(0, min(2, current_map_pos[1]))
        tiles_below_player, tiles_above_player, walls, interactables = load_map(current_map_pos)
        player.rect.topleft = (int(player.pos.x), int(player.pos.y))

    screen.fill((0, 0, 0)) # Efface l'écran

    for img, pos in tiles_below_player: # Affiche l'arrière-plan
        screen.blit(img, pos)

    for obj in interactables: # Affiche les objets Interactables
        obj.draw(screen)
    
    if(player): # Affiche le joueur
        player.draw(screen)
    
    for img, pos in tiles_above_player: # Affiche le premier plan
        screen.blit(img, pos)

    inventory_ui.draw(screen, player.inventory) # Affiche l'interface

    pygame.display.flip()
    clock.tick(60) # Bloque la fréquence de rafraichissement à 60 FPS

pygame.quit()