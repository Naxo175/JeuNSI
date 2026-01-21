import pygame
from utils import load_img
from settings import PLAYER_SIZE, PLAYER_DISPLAY_SIZE, SPEED

class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        # La hitbox reste petite pour passer dans les chemins
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.current_dir = (0, 1)
        
        # On charge les images avec la taille VISUELLE
        self.sprites = {
            (0, -1):  load_img("player_up.png", PLAYER_DISPLAY_SIZE),
            (0, 1):   load_img("player_down.png", PLAYER_DISPLAY_SIZE),
            (-1, 0):  load_img("player_left.png", PLAYER_DISPLAY_SIZE),
            (1, 0):   load_img("player_right.png", PLAYER_DISPLAY_SIZE),
            (-1, -1): load_img("player_up_left.png", PLAYER_DISPLAY_SIZE),
            (1, -1):  load_img("player_up_right.png", PLAYER_DISPLAY_SIZE),
            (-1, 1):  load_img("player_down_left.png", PLAYER_DISPLAY_SIZE),
            (1, 1):   load_img("player_down_right.png", PLAYER_DISPLAY_SIZE),
            (0, 0):   load_img("player_idle.png", PLAYER_DISPLAY_SIZE),
        }

    def move(self, dx, dy, walls):
        # ... (le code move reste identique car il utilise self.rect)
        if dx != 0 or dy != 0:
            self.current_dir = (dx, dy)
            move_vec = pygame.Vector2(dx, dy).normalize() * SPEED
            self.pos.x += move_vec.x
            self.rect.x = int(self.pos.x)
            for wall in walls:
                if self.rect.colliderect(wall):
                    if move_vec.x > 0: self.rect.right = wall.left
                    if move_vec.x < 0: self.rect.left = wall.right
                    self.pos.x = self.rect.x
            self.pos.y += move_vec.y
            self.rect.y = int(self.pos.y)
            for wall in walls:
                if self.rect.colliderect(wall):
                    if move_vec.y > 0: self.rect.bottom = wall.top
                    if move_vec.y < 0: self.rect.top = wall.bottom
                    self.pos.y = self.rect.y
    
    def check_interaction(self, interactables):
        # On crée une zone un peu plus large autour du joueur pour l'interaction
        interaction_rect = self.rect.inflate(20, 20) 
        for obj in interactables:
            if interaction_rect.colliderect(obj.rect):
                obj.interact()
                return True
        return False

    def draw(self, screen):
        sprite = self.sprites.get(self.current_dir, self.sprites[(0, 0)])
        
        # ASTUCE : On crée un rectangle pour l'image et on centre son centre 
        # sur le centre de la hitbox (self.rect)
        sprite_rect = sprite.get_rect(center=self.rect.center)
        
        screen.blit(sprite, sprite_rect)