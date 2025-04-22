###################################################################################################
# Projekt:  spaceInvaders
# Datei:    game/projectiles.py
# Autor:    Linus Wohlgemuth (Grinzold86)
# Datum:    22.4.2025
# Version:  1.1
###################################################################################################
# Beschreibung:
# Funktionen für die Verwaltung von Projektilen/Raketen
###################################################################################################

import pygame
from config import HEIGHT, ROCKET_WIDTH, ROCKET_HEIGHT, ROCKET_SPEED, ROCKET_FIRE_INTERVAL, BLUE

class ProjectileManager:
    """Klasse zur Verwaltung von Projektilen"""
    def __init__(self):
        self.projectiles = []
        self.rocket_count = 0  # Zeit seit dem letzten Schuss
    
    def update(self, dt, player, keys):
        """Aktualisiert Projektile und erstellt neue"""
        # Erhöhe den Schussintervall-Zähler
        self.rocket_count += dt * 60  # Skaliert mit dt für konsistente Feuerrate
        
        # Überprüfe, ob ein neues Projektil erstellt werden soll
        if self.rocket_count >= ROCKET_FIRE_INTERVAL:
            if keys[pygame.K_SPACE]:
                self._create_projectile(player)
                self.rocket_count = 0
        
        # Aktualisiere die Position der Projektile
        self._move_projectiles(dt)
    
    def draw(self, window):
        """Zeichnet alle Projektile"""
        for projectile in self.projectiles:
            pygame.draw.rect(window, BLUE, (projectile["x"], projectile["y"], ROCKET_WIDTH, ROCKET_HEIGHT))
    
    def _create_projectile(self, player):
        """Erstellt ein neues Projektil an der Position des Spielers"""
        projectile = {
            "x": (player.x + player.width // 2 - ROCKET_WIDTH // 2),
            "y": player.y,
            "speed": ROCKET_SPEED
        }
        self.projectiles.append(projectile)
    
    def _move_projectiles(self, dt):
        """Bewegt alle Projektile und entfernt Projektile, die den Bildschirm verlassen haben"""
        for projectile in self.projectiles[:]:  # Kopie der Liste verwenden
            projectile["y"] -= projectile["speed"] * dt  # Bewegung skaliert mit dt
            
            # Entferne Projektile, die den oberen Bildschirmrand erreicht haben
            if projectile["y"] <= 0:
                self.projectiles.remove(projectile)
    
    def get_projectiles(self):
        """Gibt die Liste der Projektile zurück"""
        return self.projectiles
    
    def remove_projectile(self, projectile):
        """Entfernt ein bestimmtes Projektil aus der Liste"""
        if projectile in self.projectiles:
            self.projectiles.remove(projectile)
    
    def reset(self):
        """Setzt den Projektil-Manager zurück"""
        self.projectiles = []
        self.rocket_count = ROCKET_FIRE_INTERVAL