###################################################################################################
# Projekt:  spaceInvaders
# Datei:    utils/highscore.py
# Autor:    Linus Wohlgemuth (Grinzold86)
# Datum:    22.4.2025
# Version:  1.1
###################################################################################################
# Beschreibung:
# Funktionen zum Laden und Speichern von Highscores
###################################################################################################

import os
import json
from config import HIGHSCORE_FILE

# Globaler Highscore
highscore = 0

def load_highscore():
    """Lädt den Highscore aus der JSON-Datei"""
    global highscore
    try:
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, "r") as f:
                data = json.load(f)
                highscore = data.get("highscore", 0)
    except Exception as e:
        print(f"Fehler beim Laden des Highscores: {e}")
        highscore = 0

def save_highscore():
    """Speichert den Highscore in der JSON-Datei"""
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"highscore": highscore}, f)
    except Exception as e:
        print(f"Fehler beim Speichern des Highscores: {e}")

def get_highscore():
    """Gibt den aktuellen Highscore zurück"""
    return highscore

def update_highscore(score):
    """Aktualisiert den Highscore wenn der neue Score höher ist"""
    global highscore
    if score > highscore:
        highscore = score
        save_highscore()
        return True
    return False

def reset_current_score():
    """Setzt den aktuellen Spielscore zurück (nicht den Highscore)"""
    global current_score
    current_score = 0

# Lade Highscore beim Import des Moduls
load_highscore()