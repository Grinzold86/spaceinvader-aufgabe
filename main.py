###################################################################################################
# Projekt:  spaceInvaders
# Datei:    main.py
# Autor:    Linus Wohlgemuth (Grinzold86)
# Datum:    22.4.2025
# Version:  1.1
###################################################################################################
# Beschreibung:
# Hauptdatei des Spiels, die alle Module zusammenführt und startet
###################################################################################################

import pygame
import sys

# Import der Konfiguration
from config import WIDTH, HEIGHT, WINDOW_TITLE

# Import der Utilities
from utils.settings import settings, load_settings
from utils.highscore import load_highscore

# Import der UI-Komponenten
from ui.menu import show_main_menu

# Import des Spielmanagers
from game.game_manager import GameManager

def main():
    """Hauptfunktion des Spiels"""
    # Pygame initialisieren
    pygame.init()
    
    # Einstellungen laden
    load_settings()
    load_highscore()
    
    # Fenster mit korrekten Flags erstellen basierend auf Einstellungen
    flags = 0
    if settings["vsync"]:
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED
    window = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    pygame.display.set_caption(WINDOW_TITLE)
    
    # Uhr für die Framerate
    clock = pygame.time.Clock()
    
    # Spielmanager erstellen
    game_manager = GameManager(window, clock)
    
    # Hauptprogrammschleife
    while True:
        # Lade den Highscore jedes Mal neu, wenn das Hauptmenü angezeigt wird
        # Dies stellt sicher, dass der aktuelle Highscore nach einem Spiel angezeigt wird
        load_highscore()
        
        # Zeigt das Hauptmenü und prüft, ob der Spieler starten möchte
        if show_main_menu(window, clock):
            # Wenn das Hauptmenü "True" zurückgibt, startet das Spiel
            game_manager.start_game()
        else:
            # Wenn das Hauptmenü "False" zurückgibt, beendet das Spiel
            break
    
    # Pygame sauber beenden und Programm schließen
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
