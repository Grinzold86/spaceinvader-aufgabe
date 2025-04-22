###################################################################################################
# Projekt:  spaceInvaders
# Datei:    ui/menu.py
# Autor:    Linus Wohlgemuth (Grinzold86)
# Datum:    22.4.2025
# Version:  1.1
###################################################################################################
# Beschreibung:
# Menüfunktionen für das Hauptmenü und die Einstellungen
###################################################################################################

import pygame
from config import (
    WIDTH, HEIGHT, BLACK, WHITE, MENU_BACKGROUND_IMAGE, 
    FRAMERATE_OPTIONS
)
from ui.button import Button
from utils.settings import settings, save_settings, load_settings
from utils.highscore import highscore, load_highscore

def show_main_menu(window, clock):
    """Zeigt das Hauptmenü an und gibt zurück, ob das Spiel gestartet werden soll"""
    # Lade den Highscore explizit neu, um den aktuellsten Wert zu erhalten
    from utils.highscore import load_highscore, highscore
    load_highscore()
    
    # Starte das Menü
    menu_running = True
    menu_background = pygame.image.load(MENU_BACKGROUND_IMAGE)
    
    while menu_running:
        # Explizit den Highscore erneut laden für den aktuellen Wert in jedem Frame
        from utils.highscore import highscore
        
        # Bildschirm zeichnen
        window.fill(BLACK)
        window.blit(menu_background, (0, 0))
        
        # Titel
        title_font = pygame.font.SysFont("Courier New", 80)
        title_text = title_font.render("SPACE INVADERS", True, WHITE)
        title_pos = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        window.blit(title_text, title_pos)
        
        # Highscore anzeigen
        highscore_font = pygame.font.SysFont("Courier New", 30)
        highscore_text = highscore_font.render(f"Highscore: {highscore}", True, WHITE)
        highscore_pos = highscore_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(highscore_text, highscore_pos)
        
        # Start-Button
        start_font = pygame.font.SysFont("Courier New", 40)
        start_text = start_font.render("Drücke SPACE zum Starten", True, WHITE)
        start_pos = start_text.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4))
        window.blit(start_text, start_pos)
        
        # Settings-Button
        settings_font = pygame.font.SysFont("Courier New", 30)
        settings_text = settings_font.render("Drücke S für Einstellungen", True, WHITE)
        settings_pos = settings_text.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4 + 50))
        window.blit(settings_text, settings_pos)
        
        # Exit-Button
        exit_font = pygame.font.SysFont("Courier New", 30)
        exit_text = exit_font.render("Drücke ESC zum Beenden", True, WHITE)
        exit_pos = exit_text.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4 + 100))
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
                if event.key == pygame.K_s:
                    show_settings_menu(window, clock)
                    # Erneut den Highscore laden, nachdem wir aus den Einstellungen zurückkehren
                    from utils.highscore import load_highscore
                    load_highscore()
                if event.key == pygame.K_ESCAPE:
                    menu_running = False
                    return False  # Spiel nicht starten
        
        clock.tick(60)

def show_settings_menu(window, clock):
    """Zeigt das Einstellungsmenü an"""
    load_settings()  # ensure we use latest saved settings
    global settings, background
    settings_running = True
    settings_background = pygame.image.load(MENU_BACKGROUND_IMAGE)
    
    # Ermittle die Bildschirmaktualisierungsrate des Monitors
    display_info = pygame.display.Info()
    monitor_refresh_rate = getattr(display_info, 'refresh_rate', 60)
    if monitor_refresh_rate <= 0:
        monitor_refresh_rate = 60  # Standardwert, falls nicht erkannt
    
    # Erstelle Buttons mit besseren Schriften
    title_font = pygame.font.SysFont("Courier New", 50)  # Kleinerer Titel
    option_font = pygame.font.SysFont("Courier New", 24)
    info_font = pygame.font.SysFont("Courier New", 14)  # Kleinere Info-Schrift
    
    # Button-Positionen - kompakteres Layout
    button_width = 280
    button_height = 40  # Kleinere Buttons
    button_x = WIDTH // 2 - button_width // 2
    
    # Kompakterer Bereich für Framerate-Buttons 
    framerate_panel = pygame.Rect(WIDTH // 6, HEIGHT // 4 - 5, WIDTH * 2 // 3, 160)
    
    # Erstelle die Framerate-Buttons in einem 3x3 Raster - kompakter
    framerate_buttons = []
    for i, rate in enumerate(FRAMERATE_OPTIONS):
        row = i // 3
        col = i % 3
        btn_width = button_width // 3 - 10
        x_pos = (WIDTH // 6) + 15 + (col * (btn_width + 15))
        y_pos = (HEIGHT // 4) + 25 + (row * 45)  # Kleinerer Abstand
        
        btn = Button(x_pos, y_pos, btn_width, button_height - 10, f"{rate} FPS", 16)
        framerate_buttons.append((btn, rate))
    
    # VSync-Button mit angepasster Positionierung
    vsync_btn = Button(button_x, HEIGHT // 4 + 180, button_width, button_height, 
                     f"VSync: {monitor_refresh_rate}Hz" if settings["vsync"] else "VSync: Aus")
    
    # FPS-Anzeige-Button
    show_fps_btn = Button(button_x, HEIGHT // 4 + 230, button_width, button_height, 
                        "FPS Anzeige: " + ("An" if settings["show_fps"] else "Aus"))
    
    # Zurück-Button mit besserem Styling
    back_btn = Button(button_x, HEIGHT // 4 + 280, button_width, button_height, "Zurück zum Hauptmenü")
    
    # Merke die ursprünglichen Einstellungen, um Änderungen zu erkennen
    original_vsync = settings["vsync"]
    window_needs_reset = False
    
    # Settings-Schleife
    while settings_running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Event-Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings()
                settings_running = False
                return False
            
            # Handle mouse clicks for buttons explicitly using event.pos
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Framerate buttons only when VSync is off
                if not settings["vsync"]:
                    for btn, rate in framerate_buttons:
                        if btn.rect.collidepoint(event.pos):
                            settings["framerate"] = rate
                            save_settings()
                            print(f"Framerate auf {rate} FPS gesetzt")
                            break
                # VSync toggle
                if vsync_btn.rect.collidepoint(event.pos):
                    settings["vsync"] = not settings["vsync"]
                    vsync_btn.text = f"VSync: {monitor_refresh_rate}Hz" if settings["vsync"] else "VSync: Aus"
                    if settings["vsync"]:
                        settings["framerate"] = monitor_refresh_rate
                    save_settings()
                    window_needs_reset = True
                # FPS display toggle
                if show_fps_btn.rect.collidepoint(event.pos):
                    settings["show_fps"] = not settings["show_fps"]
                    show_fps_btn.text = "FPS Anzeige: " + ("An" if settings["show_fps"] else "Aus")
                    save_settings()
                # Back button
                if back_btn.rect.collidepoint(event.pos):
                    save_settings()
                    settings_running = False
                    return True
            # Keyboard shortcut to exit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_settings()
                settings_running = False
                return True
        
        # Hintergrund zeichnen
        window.fill(BLACK)
        window.blit(settings_background, (0, 0))
        
        # Fancy Titel mit Schatten
        shadow_text = title_font.render("EINSTELLUNGEN", True, (40, 40, 40))
        shadow_pos = shadow_text.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 8 + 2))
        window.blit(shadow_text, shadow_pos)
        
        title_text = title_font.render("EINSTELLUNGEN", True, WHITE)
        title_pos = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 8))
        window.blit(title_text, title_pos)
        
        # Framerate-Bereich mit abgerundeten Ecken zeichnen
        pygame.draw.rect(window, (40, 40, 50), framerate_panel, border_radius=10)
        pygame.draw.rect(window, (100, 100, 120), framerate_panel, 2, border_radius=10)
        
        # Framerate-Label mit besserer Positionierung
        framerate_label = "Bildrate:"
        fr_label = option_font.render(framerate_label, True, WHITE)
        fr_label_pos = fr_label.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 5))
        window.blit(fr_label, fr_label_pos)
        
        # Info-Text für VSync
        if settings["vsync"]:
            vsync_info = info_font.render(f"VSync nutzt die Bildwiederholrate Ihres Monitors ({monitor_refresh_rate}Hz)", True, (200, 200, 200))
            vsync_info_pos = vsync_info.get_rect(center=(WIDTH // 2, framerate_panel.bottom + 10))
            window.blit(vsync_info, vsync_info_pos)
        
        # Aktuelle Auswahl-Info zeichnen
        if not settings["vsync"]:
            current_fps = option_font.render(f"Aktuelle Auswahl: {settings['framerate']} FPS", True, (200, 255, 200))
            current_fps_pos = current_fps.get_rect(center=(WIDTH // 2, framerate_panel.bottom + 10))
            window.blit(current_fps, current_fps_pos)
        
        # Framerate-Buttons zeichnen
        draw_framerate_buttons(window, framerate_buttons, mouse_pos)
        
        # VSync-Button zeichnen
        vsync_btn.is_hovered(mouse_pos)
        if vsync_btn.hovered:
            vsync_btn.draw_styled(window, (80, 80, 95), (90, 90, 105), (150, 150, 180), WHITE, 5)
        else:
            vsync_btn.draw_styled(window, (60, 60, 75), (70, 70, 85), (100, 100, 130), WHITE, 5)
        
        # FPS-Counter-Button zeichnen
        show_fps_btn.is_hovered(mouse_pos)
        if show_fps_btn.hovered:
            show_fps_btn.draw_styled(window, (80, 80, 95), (90, 90, 105), (150, 150, 180), WHITE, 5)
        else:
            show_fps_btn.draw_styled(window, (60, 60, 75), (70, 70, 85), (100, 100, 130), WHITE, 5)
        
        # Zurück-Button zeichnen
        back_btn.is_hovered(mouse_pos)
        if back_btn.hovered:
            back_btn.draw_styled(window, (90, 70, 70), (100, 80, 80), (180, 140, 140), WHITE, 5)
        else:
            back_btn.draw_styled(window, (70, 50, 50), (80, 60, 60), (140, 100, 100), WHITE, 5)
        
        pygame.display.update()
        
        # Die Framerate des Einstellungsmenüs selbst auf einen vernünftigen Wert begrenzen
        # Verwende NICHT settings["framerate"], da dies die Spielframerate ist, nicht die Menüframerate
        clock.tick(60)

def draw_framerate_buttons(window, framerate_buttons, mouse_pos):
    """Hilfsfunktion zum Zeichnen der Framerate-Buttons"""
    from utils.settings import settings
    
    for btn, rate in framerate_buttons:
        if settings["vsync"]:
            # Buttons ausgrauen bei aktivem VSync
            btn.hovered = False
            btn.draw_styled(window, (50, 50, 60), (50, 50, 60), (70, 70, 80), (100, 100, 100), 5)
        else:
            # Normal zeichnen mit Hervorhebung der aktuellen Auswahl
            if rate == settings["framerate"]:
                # Aktive Auswahl hervorheben
                btn.draw_styled(window, (60, 80, 100), (70, 90, 110), (100, 150, 200), (220, 255, 220), 5)
            else:
                # Hover-Effekt für nicht ausgewählte Buttons
                btn.is_hovered(mouse_pos)
                if btn.hovered:
                    btn.draw_styled(window, (80, 80, 95), (90, 90, 105), (150, 150, 180), WHITE, 5)
                else:
                    btn.draw_styled(window, (60, 60, 75), (70, 70, 85), (100, 100, 130), WHITE, 5)