###################################################################################################
# Projekt:  spaceInvaders
# Datei:    config.py
# Autor:    Linus Wohlgemuth (Grinzold86)
# Datum:    22.4.2025
# Version:  1.1
###################################################################################################
# Beschreibung:
# Diese Datei enthält globale Konstanten und Konfigurationen für das Spiel
###################################################################################################

import pygame

# Fenstergröße definieren
WIDTH, HEIGHT = 800, 600
WINDOW_TITLE = "Mini Space Invader"

# Pfade
SETTINGS_FILE = "settings.json"
HIGHSCORE_FILE = "highscore.json"
BACKGROUND_IMAGE = 'invaders.png'
MENU_BACKGROUND_IMAGE = 'invaders2.png'

# Farben definieren
RED = (255, 0, 0)           # Rot für das Spieler-Quadrat
BLACK = (0, 0, 0)           # Schwarz für den Hintergrund
GREEN = (0, 255, 0)         # Grün für den Feind
BLUE = (0, 0, 255)          # Blau für Projektile
WHITE = (255, 255, 255)     # Weiß für Text
GRAY = (100, 100, 100)      # Grau für Buttons
LIGHT_GRAY = (150, 150, 150) # Hellgrau für aktive Buttons

# Spieler-Eigenschaften
PLAYER_WIDTH = 40           # Breite des Spielers
PLAYER_HEIGHT = 20          # Höhe des Spielers
PLAYER_SPEED = 300          # Geschwindigkeit pro Sekunde (angepasst für dt)
PLAYER_START_Y = HEIGHT - 20 - 30  # Etwas über dem unteren Rand

# Feinde-Eigenschaften
ENEMY_WIDTH = 40            # Breite des Feindes
ENEMY_HEIGHT = 20           # Höhe des Feindes
ENEMY_SPAWN_INTERVAL = 40   # Zeiteinheiten zwischen Gegnern
ENEMY_SPEED_UP_INTERVAL = 120  # Zeiteinheiten bis zur Geschwindigkeitserhöhung

# Projektil-Eigenschaften
ROCKET_WIDTH = 5
ROCKET_HEIGHT = 10
ROCKET_SPEED = 500          # Geschwindigkeit in Pixel pro Sekunde
ROCKET_FIRE_INTERVAL = 10   # Zeiteinheiten zwischen Schüssen

# Spielphysik
BASE_FPS = 60               # Referenz-Framerate
SCROLL_SPEED = 60           # Hintergrund-Scrollgeschwindigkeit in Pixeln pro Sekunde

# Standardeinstellungen
DEFAULT_SETTINGS = {
    "framerate": 60,
    "vsync": False,
    "show_fps": False
}

# Framerate-Optionen für das Einstellungsmenü
FRAMERATE_OPTIONS = [15, 20, 30, 45, 60, 75, 120, 144, 240]