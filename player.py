import pygame
from utils import load_img
from settings import PLAYER_DISPLAY_SIZE, PLAYER_INTERACTION_AREA_SIZE, SPEED

class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y) # Position du joueur

        self.hitbox_size = (35, 35) # Dimensions de la boîte de collision
        self.hitbox_offset = pygame.Vector2(0, 25) # Décalage pour aligner la collision aux pieds
        
        self.rect = pygame.Rect(0, 0, *self.hitbox_size) # Initialisation de la hitbox
        self.update_hitbox_pos() # Position initiale de la hitbox
        
        self.current_dir = (0, 1) # Direction par défaut vers le bas
        
        self.sprites = { # Mappage des images selon les vecteurs de direction
            (0, -1):   load_img("player_up.png", PLAYER_DISPLAY_SIZE),
            (0, 1):    load_img("player_down.png", PLAYER_DISPLAY_SIZE),
            (-1, 0):   load_img("player_left.png", PLAYER_DISPLAY_SIZE),
            (1, 0):    load_img("player_right.png", PLAYER_DISPLAY_SIZE),
            (-1, -1): load_img("player_up_left.png", PLAYER_DISPLAY_SIZE),
            (1, -1):   load_img("player_up_right.png", PLAYER_DISPLAY_SIZE),
            (-1, 1):   load_img("player_down_left.png", PLAYER_DISPLAY_SIZE),
            (1, 1):    load_img("player_down_right.png", PLAYER_DISPLAY_SIZE),
            (0, 0):    load_img("player_idle.png", PLAYER_DISPLAY_SIZE),
        }

        self.inventory = [] # Liste des objets récupérés

    def move(self, dx, dy, walls):
        if dx != 0 or dy != 0:
            self.current_dir = (dx, dy) # Mise à jour de la direction
            move_vec = pygame.Vector2(dx, dy).normalize() * SPEED # Normalisation de la vitesse en diagonale
            
            # Gestion des déplacements et collisions sur l'axe X
            self.pos.x += move_vec.x
            self.update_hitbox_pos()
            for wall in walls:
                if self.rect.colliderect(wall):
                    if move_vec.x > 0: self.rect.right = wall.left
                    if move_vec.x < 0: self.rect.left = wall.right
                    self.pos.x = self.rect.centerx - self.hitbox_offset.x

            # Gestion des déplacements et collisions sur l'axe Y
            self.pos.y += move_vec.y
            self.update_hitbox_pos()
            for wall in walls:
                if self.rect.colliderect(wall):
                    if move_vec.y > 0: self.rect.bottom = wall.top
                    if move_vec.y < 0: self.rect.top = wall.bottom
                    self.pos.y = self.rect.centery - self.hitbox_offset.y
            
            self.update_hitbox_pos() # Synchronisation de la hitbox
    
    def check_interaction(self, interactables):
        # Étend la zone d'interaction autour du joueur
        interaction_rect = self.rect.inflate(PLAYER_INTERACTION_AREA_SIZE, PLAYER_INTERACTION_AREA_SIZE) 
        for obj in interactables:
            # Vérifie la proximité et l'absence de l'objet dans l'inventaire
            if interaction_rect.colliderect(obj.rect) and obj.id not in [item.id for item in self.inventory]:
                
                if obj.id == "boat": # Condition spécifique pour l'objet boat
                    pass
                else:
                    self.inventory.append(obj) # Ajout à l'inventaire du joueur

                return obj # Retourne l'objet avec lequel l'interaction a été faite
        return None
    
    def update_hitbox_pos(self):
        # Aligne le centre de la hitbox sur la position du joueur avec son décalage
        self.rect.center = self.pos + self.hitbox_offset

    def draw(self, screen):
        # Récupère le sprite correspondant à la direction
        sprite = self.sprites.get(self.current_dir, self.sprites[(0, 0)])
        
        # Centre l'image sur la position du joueur
        sprite_rect = sprite.get_rect(center=self.pos)
        screen.blit(sprite, sprite_rect)