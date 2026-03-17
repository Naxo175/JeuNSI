import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class InventoryUI:
    def __init__(self):
        self.is_open = False
        self.selected_item = None
        self.loaded_cards = {}  # Cache pour les images des cartes
        
        # Configuration des marges
        MARGIN_H, MARGIN_V = 200, 150
        self.rect = pygame.Rect(MARGIN_H, MARGIN_V, SCREEN_WIDTH - (MARGIN_H * 2), SCREEN_HEIGHT - (MARGIN_V * 2))
        
        # Chargement du fond de carte (Grille)
        try:
            raw_card_bg = pygame.image.load("sprites/cards/carte_dos.png").convert_alpha()
            self.card_bg = pygame.transform.scale(raw_card_bg, (117, 198)) # 39*3, 66*3
        except:
            self.card_bg = None
        
        self.font_medium = pygame.font.SysFont("Arial", 24)

    def toggle(self):
        self.is_open = not self.is_open

    def draw(self, screen, inventory):
        if not self.is_open: return

        # Fond principal
        pygame.draw.rect(screen, (20, 102, 0), self.rect)
        pygame.draw.rect(screen, (50, 50, 50), self.rect, 2)

        # Ligne de séparation
        separator_x = self.rect.x + int(self.rect.width * 0.7)
        pygame.draw.line(screen, (10, 10, 10), (separator_x, self.rect.y), (separator_x, self.rect.bottom), 5)

        # 1. Grille d'objets (Gauche)
        start_x, start_y = self.rect.x + 50, self.rect.y + 50
        card_w, card_h = 140, 200

        for i, item in enumerate(inventory):
            col, row = i % 5, i // 5
            x, y = start_x + col * (card_w), start_y + row * (card_h)
            item.ui_rect = pygame.Rect(x, y, card_w, card_h)

            if self.card_bg:
                screen.blit(self.card_bg, (x, y))
            
            # Icone et Nom
            icon = pygame.transform.scale(item.image, (94, 94))
            screen.blit(icon, (x + 13, y + 23))

        # 2. Affichage de la carte sélectionnée (Droite)
        if self.selected_item:
            card_img = self.loaded_cards.get(self.selected_item.id)
            if card_img:
                # Calcul pour centrer l'image dans la zone de droite
                detail_area_w = self.rect.right - separator_x
                img_rect = card_img.get_rect(center=(separator_x + detail_area_w // 2, self.rect.centery))
                screen.blit(card_img, img_rect)

    def handle_click(self, pos, inventory):
        if not self.is_open: return
        for item in inventory:
            if hasattr(item, 'ui_rect') and item.ui_rect.collidepoint(pos):
                self.selected_item = item
                
                # Charger l'image spécifique si elle n'est pas en cache
                if item.id not in self.loaded_cards:
                    try:
                        path = f"sprites/cards/carte_{item.id}.png"
                        img = pygame.image.load(path).convert_alpha()
                        # On la scale un peu plus grande pour l'affichage de droite
                        self.loaded_cards[item.id] = pygame.transform.scale(img, (234, 396))
                    except:
                        print(f"Erreur : Impossible de trouver {path}")
                break