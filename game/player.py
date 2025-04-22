###################################################################################################
# Projekt:  spaceInvaders
# Datei:    game/player.py
# Autor:    Linus Wohlgemuth (Grinzold86)
# Datum:    22.4.2025
# Version:  1.1
###################################################################################################
# Beschreibung:
# Spieler-Klasse und zugehörige Funktionen
###################################################################################################

import pygame
from config import WIDTH, HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, RED, PLAYER_START_Y

class Player:
    """Spieler-Klasse für den roten Spieler-Block"""
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.reset_position()
    
    def reset_position(self):
        """Setzt die Position des Spielers zurück"""
        self.x = WIDTH // 2 - self.width // 2
        self.y = PLAYER_START_Y
    
    def move(self, keys, dt):
        """Bewegt den Spieler basierend auf Tasteneingaben und Delta-Zeit"""
        if keys[pygame.K_LEFT]:
            self.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.x += self.speed * dt
        if keys[pygame.K_UP]:
            self.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.y += self.speed * dt
        
        # Spieler innerhalb des Fensters halten
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(400, min(HEIGHT - self.height, self.y))
    
    def draw(self, window):
        """Zeichnet den Spieler auf dem Bildschirm"""
        pygame.draw.rect(window, RED, (self.x, self.y, self.width, self.height))
    
    def collides_with(self, enemy):
        """Überprüft, ob der Spieler mit einem Gegner kollidiert"""
        return (
            abs(self.x - enemy["x"]) < self.width and 
            abs(self.y - enemy["y"]) < self.height
        )