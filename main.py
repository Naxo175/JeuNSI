import pygame
from settings import *
from utils import load_tiles_config
from player import Player
from interactable import Interactable
from inventory_ui import InventoryUI

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

TILE_CONFIG = load_tiles_config("tiles.json", TILE_SIZE)

def load_map(map_coords):
    new_walls = []
    new_floor = []
    
    data = WORLD_DATA.get(tuple(map_coords), WORLD_DATA[(0, 0)])
    
    for r, row in enumerate(data):
        for c, tile_stack in enumerate(row):
            x, y = c * TILE_SIZE, r * TILE_SIZE
            
            highest_tile_info = None
            
            # 1. On parcourt la pile pour l'affichage
            for tile_name in tile_stack:
                if tile_name == " " or not tile_name:
                    continue
                
                tile_info = TILE_CONFIG.get(tile_name)
                
                if tile_info:
                    new_floor.append((tile_info["image"], (x, y)))
                    # On mémorise cette tuile comme étant la "plus haute" actuelle
                    highest_tile_info = tile_info

            # 2. On gère la collision uniquement basée sur la tuile la plus haute
            if highest_tile_info and highest_tile_info["collision"]:
                new_walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    
    # --- Chargement des interactibles (inchangé) ---
    new_interactables = []
    objs = INTERACTABLES_DATA.get(tuple(map_coords), WORLD_DATA[0, 0])
    for x, y, id, sprite, name, description in objs:
        new_interactables.append(Interactable(x, y, id, sprite, name, description))
    
    return new_floor, new_walls, new_interactables

# Spawn configuration
START_MAP = [0, 0]
START_X = 5 * TILE_SIZE
START_Y = 6 * TILE_SIZE

current_map_pos = START_MAP

# Load start map
floor_tiles, walls, interactables = load_map(current_map_pos)

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
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

        floor_tiles, walls, interactables = load_map(current_map_pos)
        
        player.rect.topleft = (int(player.pos.x), int(player.pos.y))



    # Draw the game
    screen.fill((0, 0, 0))

    for img, pos in floor_tiles:
        screen.blit(img, pos)

    for obj in interactables:
        obj.draw(screen)
    
    if(player):
        player.draw(screen)

    inventory_ui.draw(screen, player.inventory)


    # DEBUG
    # for wall in walls:
    #     pygame.draw.rect(screen, (255, 0, 0), wall, 1)
    
    pygame.display.flip()
    clock.tick(60)


pygame.quit()