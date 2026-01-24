import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class InventoryUI:
    def __init__(self):
        self.is_open = False
        self.selected_item = None
        # Dimensions du panneau
        self.rect = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)

    def toggle(self):
        self.is_open = not self.is_open
        self.selected_item = None

    def draw(self, screen, inventory):
        if not self.is_open: return

        # Fond du panneau
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)

        # 1. Dessiner la grille (à gauche)
        start_x, start_y = self.rect.x + 20, self.rect.y + 20
        for i, item in enumerate(inventory):
            # Calculer la position dans la grille (5 colonnes)
            col = i % 5
            row = i // 5
            slot_rect = pygame.Rect(start_x + col * 90, start_y + row * 90, 80, 80)
            
            # Fond du slot
            color = (100, 100, 100) if item != self.selected_item else (241, 196, 15)
            pygame.draw.rect(screen, color, slot_rect)
            
            # Icone
            icon = pygame.transform.scale(item.image, (60, 60))
            screen.blit(icon, (slot_rect.x + 10, slot_rect.y + 10))
            
            # Stocker le rect pour le clic
            item.ui_rect = slot_rect

        # 2. Panneau de détails (à droite)
        if self.selected_item:
            detail_x = self.rect.x + 500
            # Nom
            name_txt = self.title_font.render(self.selected_item.name, True, (255, 255, 255))
            screen.blit(name_txt, (detail_x, self.rect.y + 50))
            # Image agrandie
            big_img = pygame.transform.scale(self.selected_item.image, (128, 128))
            screen.blit(big_img, (detail_x, self.rect.y + 100))
            # Description
            desc_txt = self.font.render(self.selected_item.description, True, (200, 200, 200))
            screen.blit(desc_txt, (detail_x, self.rect.y + 250))

    def handle_click(self, pos, inventory):
        if not self.is_open: return
        for item in inventory:
            if hasattr(item, 'ui_rect') and item.ui_rect.collidepoint(pos):
                self.selected_item = item
                break