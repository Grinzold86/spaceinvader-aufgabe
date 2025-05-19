###################################################################################################
# Projekt:  spaceInvaders
# Datei:    game/enemies.py
# Autor:    Linus Wohlgemuth (Grinzold86)
# Datum:    22.4.2025
# Version:  1.1
###################################################################################################
# Beschreibung:
# Funktionen für die Verwaltung von Gegnern
###################################################################################################

import pygame
import random
import logging # Import logging
from config import WIDTH, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPAWN_INTERVAL, ENEMY_SPEED_UP_INTERVAL, GREEN

logger = logging.getLogger(__name__) # Module-level logger

class EnemyManager:
    """Klasse zur Verwaltung von Gegnern"""
    def __init__(self):
        self.enemies = []
        self.count = ENEMY_SPAWN_INTERVAL  # Counter für die Erstellung neuer Gegner
        self.speed_count = 0  # Counter für die Geschwindigkeitserhöhung
        self.speed = 2  # Basisgeschwindigkeit
        
    def update(self, dt):
        """Aktualisiert den Status der Gegner und erstellt neue"""
        # Inkrementiere die Zähler basierend auf Delta-Zeit
        self.count += dt * 60  # Skaliert mit dt für konsistente Rate
        self.speed_count += dt * 60  # Skaliert mit dt für konsistente Rate

        # Überprüfe, ob ein neuer Gegner erstellt werden soll
        if self.count >= ENEMY_SPAWN_INTERVAL:
            self._spawn_enemy()
            self.count = 0

        # Überprüfe, ob die Geschwindigkeit erhöht werden soll
        if self.speed_count >= ENEMY_SPEED_UP_INTERVAL:
            self.speed += 1
            logger.info(f"Gegnergeschwindigkeit erhöht auf: {self.speed}") # Replaced print with logger.info
            self.speed_count = 0
            
        # Aktualisiere die Position der Gegner
        self._move_enemies(dt)
            
    def draw(self, window):
        """Zeichnet alle Gegner"""
        for enemy in self.enemies:
            pygame.draw.rect(window, GREEN, (enemy["x"], enemy["y"], ENEMY_WIDTH, ENEMY_HEIGHT))
    
    def _spawn_enemy(self):
        """Erstellt einen neuen Gegner"""
        base_speed = self.speed * 50  # Basisgeschwindigkeit (Pixel pro Sekunde)
        enemy = {
            "x": random.randint(0, WIDTH - ENEMY_WIDTH), 
            "y": ENEMY_HEIGHT + 20, 
            "speed": base_speed
        }
        self.enemies.append(enemy)
        
    def _move_enemies(self, dt):
        """Bewegt alle Gegner und entfernt Gegner, die den Bildschirm verlassen haben"""
        for enemy in self.enemies[:]:  # Kopie der Liste verwenden
            enemy["y"] += enemy["speed"] * dt  # Skaliert mit dt für konsistente Geschwindigkeit
            
            # Entferne Gegner, die den unteren Bildschirmrand erreicht haben
            if enemy["y"] >= (pygame.display.get_surface().get_height() - ENEMY_HEIGHT):
                self.enemies.remove(enemy)
    
    def check_collision_with_projectile(self, projectile):
        """Überprüft, ob ein Projektil mit einem Gegner kollidiert und gibt zurück, ob eine Kollision stattfand"""
        for enemy in self.enemies[:]:  # Kopie der Liste verwenden
            if (abs(projectile["x"] - enemy["x"]) < 40) and (abs(projectile["y"] - enemy["y"]) < 20):
                logger.info("Projektil hat Gegner getroffen!") # Replaced print with logger.info
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
                return True
        return False
        
    def reset(self):
        """Setzt den Gegner-Manager zurück"""
        self.enemies = []
        self.count = ENEMY_SPAWN_INTERVAL
        self.speed_count = 0
        self.speed = 2