import pygame               # Pygame-Bibliothek importieren
import sys                  # Für sys.exit()
import random              # Für Zufallszahlen (z.B. Gegner-Positionen)

pygame.init()               # Pygame initialisieren

# Fenstergröße definieren
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))      # Fenster erstellen
pygame.display.set_caption("Mini Space Invader")    # Fenstertitel setzen

# Farben definieren
RED = (255, 0, 0)           # Rot für das Spieler-Quadrat
BLACK = (0, 0, 0)           # Schwarz für den Hintergrund
GREEN = (0, 255, 0)         # Grün für den Feind
BLUE = (0, 0, 255)

# Spieler-Eigenschaften (rotes Quadrat)
player_width = 40           # Breite des Spielers
player_height = 20          # Höhe des Spielers
player_x = WIDTH // 2 - player_width // 2           # Startposition (zentriert)
player_y = HEIGHT - player_height - 30              # Etwas über dem unteren Rand
player_speed = 5            # Geschwindowdigkeit pro Frame

# Feinde-Eigenschaften (grüne Quadrate)
enemies = []
speed = 2
speedCount = 1
count = 60
enemy_width = 40           # Breite des Feindes
enemy_height = 20          # Höhe des Feindes


def enemiesSpawn():
    global count
    global speedCount
    global speed

    if count == 60:
        enemy = {"x": random.randint(0, WIDTH - enemy_width), "y": enemy_height + 20, "speed": speed}
        enemies.append(enemy)
        count = 0

    if speedCount == 60:
        speed += 1

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
    if keys[pygame.K_UP]:               # Wenn linke Pfeiltaste gedrückt
        player_y -= player_speed        # Spieler nach links bewegen
    if keys[pygame.K_DOWN]:             # Wenn rechte Pfeiltaste gedrückt
        player_y += player_speed
    if keys[pygame.K_ESCAPE]:           # Wenn "ESC" gedrückt wird
        running = False                 # Schleife beenden


# Erstellung von Schuessen
ammunition = []
rocket_width = 5
rocket_height = 10
rocketCount = 10


def projectiles():
    global rocketCount

    if rocketCount == 10:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            rockets = {"x": (player_x + 20), "y": player_y, "speed": 4}
            ammunition.append(rockets)
        rocketCount = 0
    rocketCount += 1


# Highscore anzeigen
highscore = 0


def displayHighscore():
    global highscore
    font = pygame.font.SysFont("Courier New", 20)
    score = font.render(f"Highscore: {highscore}", True, (255, 255, 255))
    position = score.get_rect(topright=(WIDTH - 10, 10))
    window.blit(score, position)


# Haupt-Spielschleife
clock = pygame.time.Clock()  # Uhr für die Framerate
running = True               # Steuerung der Schleife

while running:
    clock.tick(60)          # Max. 60 Frames pro Sekunde
    window.fill(BLACK)         # Hintergrund mit Schwarz füllen

    # Alle Events abfragen (z.B. Fenster schließen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Wenn "X" gedrückt wird
            running = False             # Schleife beenden

    keyInput()

    # Spieler innerhalb des Fensters halten
    player_x = max(0, min(WIDTH - player_width, player_x))  # Begrenzung links/rechts
    player_y = max(400, min(HEIGHT - player_height, player_y))  # Begrenzung oben/unten

    # Spieler-Quadrat zeichnen
    pygame.draw.rect(window, RED, (player_x, player_y, player_width, player_height))
  
    projectiles()

    for rockets in ammunition:
        rockets["y"] -= rockets["speed"]

        rockets["y"] = max(0, min(HEIGHT - enemy_height, rockets["y"]))

        if (rockets["y"] == (0)):
            ammunition.remove(rockets)

        pygame.draw.rect(window, BLUE, (rockets["x"], rockets["y"], rocket_width, rocket_height))

        for enemy in enemies:
            if (abs(rockets["x"] - enemy["x"]) < 40) and (abs(rockets["y"] - enemy["y"]) < 20):
                print("TREFFER!")
                ammunition.remove(rockets)
                enemies.remove(enemy)
                highscore += 1
 
    # Gegner erstellen
    enemiesSpawn()

    for enemy in enemies:
        enemy["y"] += enemy["speed"]

        enemy["y"] = max(0, min(HEIGHT - enemy_height, enemy["y"]))

        if (enemy["y"] == (HEIGHT - enemy_height)):
            enemies.remove(enemy)

        pygame.draw.rect(window, GREEN, (enemy["x"], enemy["y"], enemy_width, enemy_height))

        if (abs(enemy["x"] - player_x) < 40) and (abs(enemy["y"] - player_y) < 20):
            print("Kollision detektiert")
            running = False
            gameOver()

    displayHighscore()
    pygame.display.update()             # Anzeige aktualisieren

pygame.quit()               # Pygame sauber beenden
sys.exit()                  # Programm beenden
