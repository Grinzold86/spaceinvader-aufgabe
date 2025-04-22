# Space Invaders Game

## Overview
Space Invaders is a classic arcade game implemented in Python using the Pygame library. This project demonstrates core game development concepts with a modular structure.

## Features
- Classic Space Invaders gameplay
- Persistent highscore system (`highscore.json`)
- Main menu screen
- Configurable settings via `settings.json` (framerate, vsync, show FPS)
- Progressive difficulty (enemies speed up over time)
- Smooth scrolling background
- Modular project structure for better organization

## How to Play
1. Launch the game by running `main.py`
2. Use the main menu to start the game or adjust settings (if implemented).
3. Controls:
   - Arrow keys (←, →) to move your ship
   - SPACE to fire projectiles
   - ESC to exit the game (saves highscore if applicable)
4. Shoot the alien invaders to score points.
5. Avoid collisions with the aliens.
6. Your highscore is automatically saved when the game ends or you exit via ESC.

## Requirements
- Python 3.x
- Pygame library

## Installation
1. Make sure you have Python installed.
2. Install Pygame using pip:
```powershell
pip install pygame
```
3. Run the game:
```powershell
python main.py
```

## Configuration
- `config.py`: Contains core game constants like screen dimensions, colors, and image paths.
- `settings.json`: Allows customization of framerate, VSync, and FPS counter visibility. Modify this file to change these settings.

## Project Structure
- `main.py`: The main entry point of the application. Initializes Pygame, loads resources, and manages the main game loop (menu and game).
- `config.py`: Stores configuration constants.
- `highscore.json`: Stores the persistent highscore.
- `settings.json`: Stores user-configurable settings.
- `invaders.png`: Background image for the gameplay screen.
- `invaders2.png`: Background image for the main menu.
- `game/`: Contains core gameplay logic.
    - `game_manager.py`: Manages the main game state, updates, drawing, and collision detection.
    - `player.py`: Defines the player ship class.
    - `enemies.py`: Defines the enemy class and manages enemy waves.
    - `projectiles.py`: Defines the projectile class and manages player shots.
- `ui/`: Contains user interface elements.
    - `menu.py`: Implements the main menu screen.
    - `button.py`: (If present) Defines reusable button components.
- `utils/`: Contains helper modules.
    - `settings.py`: Handles loading and saving settings from `settings.json`.
    - `highscore.py`: Handles loading, saving, and updating the highscore from `highscore.json`.
- `hilfe.py`: Helper script (if any specific purpose).

## Credits
Created by Linus Wohlgemuth (Grinzold86)
Date: April 22, 2025
Version: 1.1

## License
This project is intended for educational purposes only.