###################################################################################################
# Projekt:  spaceInvaders
# Datei:    game/game_manager.py
# Autor:    Linus Wohlgemuth (Grinzold86)
# Datum:    22.4.2025
# Version:  1.1
###################################################################################################
# Beschreibung:
# Hauptspiel-Manager zur Steuerung des Spielablaufs
###################################################################################################

import pygame
import sys
import logging # Import the logging module

from config import WIDTH, HEIGHT, BLACK, WHITE, BACKGROUND_IMAGE, BASE_FPS, SCROLL_SPEED
from game.player import Player
from game.enemies import EnemyManager
from game.projectiles import ProjectileManager
from utils.settings import settings, save_settings
from utils.highscore import highscore, save_highscore, update_highscore

logger = logging.getLogger(__name__) # Logger instance for this module

class GameManager:
    """Verwaltet den Spielablauf und koordiniert alle Spielelemente"""
    
    def __init__(self, window, clock):
        self.window = window
        self.clock = clock
        self.background = pygame.image.load(BACKGROUND_IMAGE)
        self.running = False
        self.score = 0
        self.dt = 1 / BASE_FPS  # Delta-Zeit für framerate-unabhängige Bewegung
        
        # Spielobjekte initialisieren
        self.player = Player()
        self.enemy_manager = EnemyManager()
        self.projectile_manager = ProjectileManager()
        
        # Hintergrund-Scrolling
        self.bg_x = 0.0  # use float for smooth scrolling
        
    def start_game(self):
        """Startet eine neue Spielrunde"""
        self.running = True
        self.score = 0  # Setze Spielpunkte auf 0
        
        # Zurücksetzen aller Spielobjekte
        self.player.reset_position()
        self.enemy_manager.reset()
        self.projectile_manager.reset()
        self.bg_x = 0
        
        # Hauptspielschleife ausführen
        self.game_loop()
    
    def game_loop(self):
        """Die Hauptspielschleife"""
        while self.running:
            # Event-Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game(should_save_score=True) # Spielstand speichern beim Schließen
                    pygame.quit()
                    sys.exit()
            
            # Zeichnen und Taktgebung für den Frame durch die Uhr
            # Dies begrenzt die Framerate auf den eingestellten Wert
            current_framerate = settings["framerate"]
            self.clock.tick(current_framerate)
            
            # Berechne Delta-Zeit (dt) für framerate-unabhängige Bewegung
            # Standard-Ziel-dt basierend auf der aktuellen Framerate-Einstellung
            if current_framerate > 0:
                target_dt = 1.0 / current_framerate
            else:
                # Fallback auf BASE_FPS, wenn current_framerate ungültig ist (z.B. 0)
                target_dt = 1.0 / BASE_FPS # BASE_FPS sollte eine positive Konstante sein
            
            if settings["show_fps"]:
                # Wenn FPS angezeigt werden, verwende die tatsächlich verstrichene Zeit.
                # Dies kann zu variablerem dt führen, spiegelt aber die reale Performance wider.
                actual_elapsed_time_sec = self.clock.get_time() / 1000.0
                
                # Verwende die tatsächliche Zeit, wenn sie positiv ist; andernfalls den Ziel-dt.
                # Dies verhindert, dass dt Null wird, was zeitabhängige Aktualisierungen anhalten könnte.
                self.dt = actual_elapsed_time_sec if actual_elapsed_time_sec > 0 else target_dt
            else:
                # Wenn FPS nicht angezeigt werden, verwende einen festen dt basierend auf der Ziel-Framerate.
                # Dies sorgt für konsistentere und vorhersagbarere Physik.
                self.dt = target_dt
            
            # Spiellogik aktualisieren
            self.update()
            
            # Zeichnen
            self.draw()
    
    def update(self):
        """Aktualisiert die Spiellogik für einen Frame"""
        keys = pygame.key.get_pressed()
        
        # Spieler-Eingabe und Bewegung
        if keys[pygame.K_ESCAPE]:
            # Explizit should_save_score=True setzen, um sicherzustellen, dass der Highscore gespeichert wird
            self.end_game(should_save_score=True)
            return
        
        # Spieler bewegen
        self.player.move(keys, self.dt)
        
        # Projektile aktualisieren und neue erstellen
        self.projectile_manager.update(self.dt, self.player, keys)
        
        # Gegner aktualisieren und neue erstellen
        self.enemy_manager.update(self.dt)
        
        # Kollisionserkennung
        self.check_collisions()
        
        # Hintergrund-Scrolling aktualisieren
        # smooth subpixel scrolling
        self.bg_x -= SCROLL_SPEED * self.dt
        # stop wrap exactly at image width to prevent overshoot
        bg_width = self.background.get_width()
        if self.bg_x <= -bg_width:
            self.bg_x = 0.0
    
    def draw(self):
        """Zeichnet einen Frame"""
        # Hintergrund
        self.window.fill(BLACK)
        # Endless background: draw two images side by side
        bg_width = self.background.get_width()
        x = int(self.bg_x)
        self.window.blit(self.background, (x, 0))
        self.window.blit(self.background, (x + bg_width, 0))

        # Spielelemente
        self.player.draw(self.window)
        self.enemy_manager.draw(self.window)
        self.projectile_manager.draw(self.window)
        
        # UI-Elemente
        self.draw_score()
        self.draw_fps()
        
        # Anzeige aktualisieren
        pygame.display.update()
    
    def check_collisions(self):
        """Überprüft Kollisionen zwischen Spielobjekten"""
        # Projektile mit Gegnern
        for projectile in self.projectile_manager.get_projectiles()[:]:
            if self.enemy_manager.check_collision_with_projectile(projectile):
                self.projectile_manager.remove_projectile(projectile)
                self.score += 1
        
        # Spieler mit Gegnern
        for enemy in self.enemy_manager.enemies[:]:
            if self.player.collides_with(enemy):
                logger.info("Kollision zwischen Spieler und Gegner detektiert.") # Replaced print with logger.info
                self.end_game(game_over=True, should_save_score=True) # Corrected argument name
                break
    
    def draw_score(self):
        """Zeichnet den aktuellen Score"""
        font = pygame.font.SysFont("Courier New", 20)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        position = score_text.get_rect(topright=(WIDTH - 10, 10))
        self.window.blit(score_text, position)
    
    def draw_fps(self):
        """Zeichnet die aktuelle FPS-Anzeige wenn aktiviert"""
        if settings["show_fps"]:
            fps = round(self.clock.get_fps())
            fps_font = pygame.font.SysFont("Courier New", 20)
            fps_text = fps_font.render(f"FPS: {fps}", True, WHITE)
            position = fps_text.get_rect(topleft=(10, 10))
            self.window.blit(fps_text, position)
    
    def end_game(self, game_over=False, should_save_score=False):
        """Beendet das Spiel, optional speichert den Score und zeigt entsprechende Screens."""
        self.running = False
        
        achieved_new_highscore = False
        if should_save_score:
            # Aktualisiere Highscore wenn nötig und speichere ihn sofort
            if self.score > 0:  # Nur wenn Punkte erzielt wurden
                achieved_new_highscore = update_highscore(self.score)
                if achieved_new_highscore:
                    logger.info(f"Neuer Highscore: {self.score}") # Replaced print with logger.info
                else:
                    # highscore wird aus utils.highscore importiert und enthält den aktuellen Highscore-Wert
                    logger.info(f"Aktueller Score: {self.score}, Highscore bleibt: {highscore}") # Replaced print with logger.info
                
                # Sicherstellen, dass der Highscore gespeichert wird, falls should_save_score True ist und Punkte erzielt wurden
                save_highscore()
        
        if game_over:
            self.show_game_over()
        elif achieved_new_highscore:
            # Diese Bedingung impliziert, dass should_save_score True war, self.score > 0 und ein neuer Highscore erzielt wurde.
            # Zeige eine Benachrichtigung, wenn es kein Game Over war, aber ein neuer Highscore erzielt wurde
            # (z.B. Spiel per ESC beendet mit neuem Highscore).
            self.show_highscore_notification()
    
    def show_game_over(self):
        """Zeigt den Game Over Screen"""
        self.window.fill(BLACK)
        font = pygame.font.SysFont("Courier New", 80)
        text = font.render("Spiel Vorbei", True, WHITE)
        position = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.window.blit(text, position)
        pygame.display.flip()
        pygame.time.wait(1000)
    
    def show_highscore_notification(self):
        """Zeigt eine Benachrichtigung über einen neuen Highscore"""
        self.window.fill(BLACK)
        
        # Erster Text: Neuer Highscore
        font_large = pygame.font.SysFont("Courier New", 60)
        text_large = font_large.render("NEUER HIGHSCORE!", True, (255, 215, 0))  # Gold-Farbe
        position_large = text_large.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        
        # Zweiter Text: Punktestand
        font_score = pygame.font.SysFont("Courier New", 40)
        text_score = font_score.render(f"{self.score} Punkte", True, WHITE)
        position_score = text_score.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Einfache Anzeige ohne Animation
        self.window.blit(text_large, position_large)
        self.window.blit(text_score, position_score)
        
        pygame.display.flip()
        
        # Warte kurz, damit der Spieler die Mitteilung lesen kann
        pygame.time.wait(2000)