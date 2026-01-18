import pygame
from settings import *
from utils import load_img
from player import Player

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Chargement textures tiles
tile_images = {
    'W': load_img("wall.png", TILE_SIZE),
    'G': load_img("grass.png", TILE_SIZE),
    'D': load_img("dirt.png", TILE_SIZE),
    'B': load_img("wood.png", TILE_SIZE),
}

# Génération niveau
walls = []
floor_tiles = []
player = None

for r, row in enumerate(MAP_DATA):
    for c, char in enumerate(row):
        x, y = c * TILE_SIZE, r * TILE_SIZE
        if char == 'P':
            player = Player(x, y)
            char = 'G'
        
        tile_char = char if char in tile_images else 'G'
        floor_tiles.append((tile_images[tile_char], (x, y)))
        
        if char in COLLISION_TILES:
            walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Inputs
    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] or keys[pygame.K_d] - keys[pygame.K_q]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP] or keys[pygame.K_s] - keys[pygame.K_z]

    # Update
    if player:
        player.move(dx, dy, walls)

    # Draw
    screen.fill((0, 0, 0))
    for img, pos in floor_tiles:
        screen.blit(img, pos)
    
    if player:
        player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()