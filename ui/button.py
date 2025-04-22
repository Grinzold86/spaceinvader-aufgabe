###################################################################################################
# Projekt:  spaceInvaders
# Datei:    ui/button.py
# Autor:    Linus Wohlgemuth (Grinzold86)
# Datum:    22.4.2025
# Version:  1.1
###################################################################################################
# Beschreibung:
# Button-Klasse für das UI
###################################################################################################

import pygame
from config import WHITE, GRAY, LIGHT_GRAY

class Button:
    """Button-Klasse für Menüs und UI"""
    def __init__(self, x, y, width, height, text, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont("Courier New", font_size)
        self.hovered = False
        
    def draw(self, surface):
        """Zeichnet den Button auf der angegebenen Oberfläche"""
        color = LIGHT_GRAY if self.hovered else GRAY
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)  # Border
        
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def draw_styled(self, surface, normal_color, hover_color, border_color, text_color=WHITE, border_radius=0):
        """Zeichnet einen stilisierten Button mit angepassten Farben und abgerundeten Ecken"""
        color = hover_color if self.hovered else normal_color
        pygame.draw.rect(surface, color, self.rect, border_radius=border_radius)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=border_radius)
        
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def is_hovered(self, mouse_pos):
        """Überprüft, ob der Mauszeiger über dem Button ist"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered
        
    def is_clicked(self, event):
        """Überprüft, ob der Button geklickt wurde"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.hovered
        return False