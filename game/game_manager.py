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

from config import WIDTH, HEIGHT, BLACK, WHITE, BACKGROUND_IMAGE, BASE_FPS, SCROLL_SPEED
from game.player import Player
from game.enemies import EnemyManager
from game.projectiles import ProjectileManager
from utils.settings import settings, save_settings
from utils.highscore import highscore, save_highscore, update_highscore

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
                    self.end_game(save=True)
                    pygame.quit()
                    sys.exit()
            
            # Zeichnen und Taktgebung für den Frame durch die Uhr
            # Dies begrenzt die Framerate auf den eingestellten Wert
            current_framerate = settings["framerate"]
            self.clock.tick(current_framerate)
            
            # Berechne Delta-Zeit (dt) für framerate-unabhängige Bewegung
            # Wenn show_fps aktiviert ist, verwende die tatsächliche verstrichene Zeit
            if settings["show_fps"]:
                # Verwende die tatsächlich verstrichene Zeit (in Sekunden)
                actual_dt = self.clock.get_time() / 1000.0
                if actual_dt > 0:  # Vermeide Division durch Null
                    self.dt = actual_dt
            else:
                # Standardwert basierend auf Ziel-Framerate
                self.dt = 1 / current_framerate
            
            # Spiellogik aktualisieren
            self.update()
            
            # Zeichnen
            self.draw()
    
    def update(self):
        """Aktualisiert die Spiellogik für einen Frame"""
        keys = pygame.key.get_pressed()
        
        # Spieler-Eingabe und Bewegung
        if keys[pygame.K_ESCAPE]:
            # Explizit save=True setzen, um sicherzustellen, dass der Highscore gespeichert wird
            self.end_game(save=True)
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
                print("Kollision detektiert")
                self.end_game(game_over=True, save=True)
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
    
    def end_game(self, game_over=False, save=False):
        """Beendet das Spiel"""
        self.running = False
        
        is_new_highscore = False
        if save:
            # Aktualisiere Highscore wenn nötig und speichere ihn sofort
            if self.score > 0:  # Nur wenn Punkte erzielt wurden
                is_new_highscore = update_highscore(self.score)
                if is_new_highscore:
                    print(f"Neuer Highscore: {self.score}")
                else:
                    print(f"Aktueller Score: {self.score}, Highscore bleibt: {highscore}")
                
                # Sicherstellen, dass der Highscore gespeichert wird
                save_highscore()
        
        if game_over:
            self.show_game_over()
        elif save and is_new_highscore:
            # Wenn kein Game-Over, aber ein neuer Highscore beim Beenden mit ESC, zeige Highscore-Mitteilung
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