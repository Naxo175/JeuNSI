import pygame
from utils import load_img
from settings import PLAYER_DISPLAY_SIZE, SPEED

class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)

        # PARAMÈTRES AVANCÉS
        self.hitbox_size = (35, 25)
        # Décalage (x, y) du centre de la hitbox par rapport à self.pos
        # Un y_offset de -10 monte la hitbox, un y_offset de 10 la descend
        self.hitbox_offset = pygame.Vector2(0, 25) 
        
        # Création initiale du rectangle
        self.rect = pygame.Rect(0, 0, *self.hitbox_size)
        self.update_hitbox_pos()
        
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
        if dx != 0 or dy != 0:
            self.current_dir = (dx, dy)
            move_vec = pygame.Vector2(dx, dy).normalize() * SPEED
            
            # Axe X
            self.pos.x += move_vec.x
            self.update_hitbox_pos()
            for wall in walls:
                if self.rect.colliderect(wall):
                    if move_vec.x > 0: self.rect.right = wall.left
                    if move_vec.x < 0: self.rect.left = wall.right
                    # On replace le point de position selon la nouvelle position du rect
                    self.pos.x = self.rect.centerx - self.hitbox_offset.x

            # Axe Y
            self.pos.y += move_vec.y
            self.update_hitbox_pos()
            for wall in walls:
                if self.rect.colliderect(wall):
                    if move_vec.y > 0: self.rect.bottom = wall.top
                    if move_vec.y < 0: self.rect.top = wall.bottom
                    self.pos.y = self.rect.centery - self.hitbox_offset.y
            
            self.update_hitbox_pos() # Toujours finir par synchroniser
    
    def check_interaction(self, interactables):
        # On crée une zone un peu plus large autour du joueur pour l'interaction
        interaction_rect = self.rect.inflate(20, 20) 
        for obj in interactables:
            if interaction_rect.colliderect(obj.rect):
                obj.interact()
                return True
        return False
    
    def update_hitbox_pos(self):
        # On centre la hitbox sur self.pos, puis on applique l'offset
        self.rect.center = self.pos + self.hitbox_offset

    def draw(self, screen):
        sprite = self.sprites.get(self.current_dir, self.sprites[(0, 0)])
        
        # On aligne le bas du sprite sur le point de position logique
        sprite_rect = sprite.get_rect(center=self.pos)
        screen.blit(sprite, sprite_rect)

        # DEBUG
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)