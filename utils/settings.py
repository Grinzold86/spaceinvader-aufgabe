###################################################################################################
# Projekt:  spaceInvaders
# Datei:    utils/settings.py
# Autor:    Linus Wohlgemuth (Grinzold86)
# Datum:    22.4.2025
# Version:  1.1
###################################################################################################
# Beschreibung:
# Funktionen zum Laden und Speichern von Spieleinstellungen
###################################################################################################

import os
import json
from config import DEFAULT_SETTINGS, SETTINGS_FILE

# Globale Einstellungen
settings = DEFAULT_SETTINGS.copy()

def load_settings():
    """Lädt Einstellungen aus der JSON-Datei"""
    global settings
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                loaded_settings = json.load(f)
                # Update our settings with loaded values, keeping defaults for any missing keys
                for key in loaded_settings:
                    if key in settings:
                        settings[key] = loaded_settings[key]
    except Exception as e:
        print(f"Fehler beim Laden der Einstellungen: {e}")

def save_settings():
    """Speichert Einstellungen in der JSON-Datei"""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)
    except Exception as e:
        print(f"Fehler beim Speichern der Einstellungen: {e}")

def get_setting(key):
    """Gibt den Wert einer bestimmten Einstellung zurück"""
    return settings.get(key, DEFAULT_SETTINGS.get(key))

def update_setting(key, value):
    """Aktualisiert eine Einstellung und speichert sie"""
    if key in settings:
        settings[key] = value
        save_settings()
        return True
    return False

# Lade Einstellungen beim Import des Moduls
load_settings()