import pygame
from settings import *
from utils import load_tiles_config
from player import Player
from interactable import Interactable

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

TILE_CONFIG = load_tiles_config("tiles.json", TILE_SIZE)

def load_map(map_coords):
    new_walls = []
    new_floor = []
    
    data = WORLD_DATA.get(tuple(map_coords), WORLD_DATA[(0,0)])
    
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            x, y = c * TILE_SIZE, r * TILE_SIZE
            
            tile_info = TILE_CONFIG.get(char, TILE_CONFIG['1'])

            new_floor.append((tile_info["image"], (x, y)))
            
            if tile_info["collision"]:
                new_walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    
    # Load interactables of this map
    new_interactables = []
    objs = INTERACTABLES_DATA.get(tuple(map_coords), [])
    for x, y, sprite, msg in objs:
        new_interactables.append(Interactable(x, y, sprite, msg))
    
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



    # Inputs and Movement
    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] or keys[pygame.K_d] - keys[pygame.K_q]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP] or keys[pygame.K_s] - keys[pygame.K_z]
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
    
    if(player):
        player.draw(screen)
    
    for obj in interactables:
        obj.draw(screen)

    # DEBUG
    # for wall in walls:
    #     pygame.draw.rect(screen, (255, 0, 0), wall, 1)
    
    pygame.display.flip()
    clock.tick(60)


pygame.quit()