###################################################################################################
# Projekt:  spaceInvaders
# Datei:    main.py
# Autor:    Linus Wohlgemuth (Grinzold86)
# Datum:    4.3.2025
# Version:  1.0
###################################################################################################
# Beschreibung:
# Diese Projekt dient zur Übung und soll die Möglichkeiten mit pygame aufzeigen
###################################################################################################

import pygame               # Pygame-Bibliothek importieren
import sys                  # Für sys.exit()
import random               # Für Zufallszahlen (z.B. Gegner-Positionen)
import os                   # Für Dateizugriff (Highscore-Datei)
import json                 # Für das Speichern des Highscores als JSON

pygame.init()               # Pygame initialisieren

# Fenstergröße definieren
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load('invaders.png')      # Fenster erstellen
pygame.display.set_caption("Mini Space Invader")    # Fenstertitel setzen

# Farben definieren
RED = (255, 0, 0)           # Rot für das Spieler-Quadrat
BLACK = (0, 0, 0)           # Schwarz für den Hintergrund
GREEN = (0, 255, 0)         # Grün für den Feind
BLUE = (0, 0, 255)          # Blau für Projektile

# Spieler-Eigenschaften (rotes Rechteck)
player_width = 40           # Breite des Spielers
player_height = 20          # Höhe des Spielers
player_speed = 5            # Geschwindigkeit pro Frame

# Feinde-Eigenschaften (grüne Rechtecke)
enemy_width = 40           # Breite des Feindes
enemy_height = 20          # Höhe des Feindes

# Projektil-Eigenschaften (blaue Rechtecke)
rocket_width = 5
rocket_height = 10

# Highscore und Pfad für die Highscore-Datei
highscore = 0
HIGHSCORE_FILE = "highscore.json"

# Uhr für die Framerate
clock = pygame.time.Clock()

def enemiesSpawn():
    global count
    global speedCount
    global speed
    global enemies

    if count == 40:             # erstellt alle 60 frames einen Gegner
        enemy = {"x": random.randint(0, WIDTH - enemy_width), "y": enemy_height + 20, "speed": speed}
        enemies.append(enemy)
        count = 0

    if speedCount == 120:
        speed += 1
        print("Erhöht")
        speedCount = 0

    speedCount += 1
    count += 1


def gameOver():
    window.fill(BLACK)
    font = pygame.font.SysFont("Courier New", 80)
    text = font.render("Game Over", True, (255, 255, 255))
    position = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(text, position)
    pygame.display.flip()
    pygame.time.wait(1000)
    # Save the highscore before returning to main menu
    save_highscore()


# Funktion für die Erkennung der Tasteneingabe
def keyInput():
    global running
    global player_x
    global player_y

    # Tasteneingaben abfragen
    keys = pygame.key.get_pressed()     # Aktuell gedrückte Tasten
    if keys[pygame.K_LEFT]:             # Wenn linke Pfeiltaste gedrückt
        player_x -= player_speed        # Spieler nach links bewegen
    if keys[pygame.K_RIGHT]:            # Wenn rechte Pfeiltaste gedrückt
        player_x += player_speed        # Spieler nach rechts bewegen
    if keys[pygame.K_UP]:               # Wenn obere Pfeiltaste gedrückt
        player_y -= player_speed        # Spieler nach oben bewegen
    if keys[pygame.K_DOWN]:             # Wenn untere Pfeiltaste gedrückt
        player_y += player_speed        # Spieler nach unten bewegen
    if keys[pygame.K_ESCAPE]:           # Wenn "ESC" gedrückt wird
        running = False                 # Spiel beenden


def projectiles():
    global rocketCount
    global ammunition

    if rocketCount == 10:               # if-Verzweigung verhindert dass ein Strahl an Raketen gefeuert wird
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            rockets = {"x": (player_x + 20), "y": player_y, "speed": 4}
            ammunition.append(rockets)
        rocketCount = 0
    rocketCount += 1


# Funktion zum Laden des Highscores
def load_highscore():
    global highscore
    try:
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, "r") as f:
                data = json.load(f)
                highscore = data.get("highscore", 0)
    except Exception as e:
        print(f"Fehler beim Laden des Highscores: {e}")
        highscore = 0

# Funktion zum Speichern des Highscores
def save_highscore():
    global highscore
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"highscore": highscore}, f)
    except Exception as e:
        print(f"Fehler beim Speichern des Highscores: {e}")

def displayHighscore():
    global highscore
    font = pygame.font.SysFont("Courier New", 20)
    score = font.render(f"Highscore: {highscore}", True, (255, 255, 255))
    position = score.get_rect(topright=(WIDTH - 10, 10))
    window.blit(score, position)

# Funktion für den Hauptbildschirm
def show_main_menu():
    # Lade den Highscore beim Start
    load_highscore()
    
    menu_running = True
    menu_background = pygame.image.load('invaders2.png')
    
    while menu_running:
        window.fill(BLACK)
        window.blit(menu_background, (0, 0))
        
        # Titel
        title_font = pygame.font.SysFont("Courier New", 80)
        title_text = title_font.render("SPACE INVADERS", True, (255, 255, 255))
        title_pos = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        window.blit(title_text, title_pos)
        
        # Highscore anzeigen
        highscore_font = pygame.font.SysFont("Courier New", 30)
        highscore_text = highscore_font.render(f"Highscore: {highscore}", True, (255, 255, 255))
        highscore_pos = highscore_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(highscore_text, highscore_pos)
        
        # Start-Button
        start_font = pygame.font.SysFont("Courier New", 40)
        start_text = start_font.render("Press SPACE to Start", True, (255, 255, 255))
        start_pos = start_text.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4))
        window.blit(start_text, start_pos)
        
        # Exit-Button
        exit_font = pygame.font.SysFont("Courier New", 30)
        exit_text = exit_font.render("Press ESC to Exit", True, (255, 255, 255))
        exit_pos = exit_text.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4 + 50))
        window.blit(exit_text, exit_pos)
        
        pygame.display.update()
        
        # Event-Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                return False  # Spiel nicht starten
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_running = False
                    return True  # Spiel starten
                if event.key == pygame.K_ESCAPE:
                    menu_running = False
                    return False  # Spiel nicht starten
        
        clock.tick(60)

# Hauptprogrammschleife
while True:
    # Zeige Hauptmenü und prüfe, ob Spieler starten möchte
    if show_main_menu() == False:
        break  # Beende das Spiel, wenn der Spieler nicht starten möchte
    
    # Spiel-Initialisierung für jede neue Runde
    enemies = []
    ammunition = []
    speed = 2
    speedCount = 1
    count = 40
    rocketCount = 10
    x = 0
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 30
    running = True
    
    # Die eigentliche Spielschleife
    while running:
        clock.tick(60)          # Max. 60 Frames pro Sekunde
        
        # Alle Events abfragen (z.B. Fenster schließen) - Jetzt außerhalb des if-Blocks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Wenn "X" gedrückt wird
                save_highscore()
                pygame.quit()               # Pygame sauber beenden
                sys.exit()                  # Programm beenden
                
        # Tasteneingaben jetzt in jedem Frame verarbeiten
        keyInput()
        
        # Hintergrund mit Bild füllen
        window.blit(background, (x, 0))
        x -= 1
        if x == -700:
            x = 0

        # Spieler innerhalb des Fensters halten
        player_x = max(0, min(WIDTH - player_width, player_x))  # Begrenzung links/rechts
        player_y = max(400, min(HEIGHT - player_height, player_y))  # Begrenzung oben/unten

        # Spieler-Quadrat zeichnen
        pygame.draw.rect(window, RED, (player_x, player_y, player_width, player_height))

        projectiles()

        for rockets in ammunition[:]:          # Kopie der Liste verwenden, um Fehler beim Entfernen zu vermeiden
            rockets["y"] -= rockets["speed"]

            rockets["y"] = max(0, min(HEIGHT - enemy_height, rockets["y"]))

            if (rockets["y"] == (0)):
                ammunition.remove(rockets)
                continue

            pygame.draw.rect(window, BLUE, (rockets["x"], rockets["y"], rocket_width, rocket_height))

            for enemy in enemies[:]:  # Kopie der Liste verwenden
                if (abs(rockets["x"] - enemy["x"]) < 40) and (abs(rockets["y"] - enemy["y"]) < 20):
                    print("TREFFER!")
                    if rockets in ammunition:
                        ammunition.remove(rockets)
                    if enemy in enemies:
                        enemies.remove(enemy)
                    highscore += 1
                    break

        # Gegner erstellen
        enemiesSpawn()

        for enemy in enemies[:]:                   # Kopie der Liste verwenden
            enemy["y"] += enemy["speed"]

            enemy["y"] = max(0, min(HEIGHT - enemy_height, enemy["y"]))

            if (enemy["y"] == (HEIGHT - enemy_height)):
                enemies.remove(enemy)
                continue

            pygame.draw.rect(window, GREEN, (enemy["x"], enemy["y"], enemy_width, enemy_height))

            if (abs(enemy["x"] - player_x) < 40) and (abs(enemy["y"] - player_y) < 20):
                print("Kollision detektiert")
                running = False
                gameOver()
                break  # Beende die Schleife nach einer Kollision

        displayHighscore()
        pygame.display.update()             # Anzeige aktualisieren

pygame.quit()               # Pygame sauber beenden
sys.exit()                  # Programm beenden
