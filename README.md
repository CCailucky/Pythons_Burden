# Python's Burden: Escape from COMP9001

## Overview

**Python's Burden: Escape from COMP9001** is a Pygame-based snake adventure game developed for a Python programming final project

The player controls Python, a little snake trapped in the COMP9001 maze. The goal is to collect letters in the correct order, use items and bullets, survive guardian snakes, complete the target sequence, and enter the escape portal to win the game.
## Requirements

- Python 3.11 or later is recommended.
- `pygame-ce`

This project uses `pygame-ce`, but it is imported in the code as `pygame`.

Install the required dependency with:

```bash
python -m pip install pygame-ce
```

## How to Run

1. Clone or download this project.
```bash
git clone https://github.com/CCailucky/Pythons_Burden.git
cd Pythons_Burden
```
2. Install the required dependency.
```bash
python -m pip install pygame-ce
```
3. Run the game.
```bash
python main.py
```
If your system uses `python3`, run:
```bash
python3 main.py
```
## Features
- Start interface with mouse-controlled buttons
- Multi-page rules introduction screens
- Responsive window scaling
- Grid-based snake movement
- Quantum teleport at map edges
- Letter collection and target sequence system
- Wildcard letter system
- TailCut item system
- Bullet shooting system
- BulletSupply item system
- Enemy snake AI
- Enemy drops after defeat
- Exit portal win condition
- Pause menu with keyboard and mouse controls
- Pixel-art assets and custom UI panels

## How to Play

1. Click **Start** on the start interface to enter the game.

2. Control Python with the arrow keys and collect letters in the correct order to match the target sequence.

3. Each collected letter is added to Python's body. Eating a letter also makes Python grow by one segment.

4. Use special items to help you:
   - **Wildcard Letter** becomes the next required letter in the sequence.
   - **TailCut** removes 1-3 collected letters and cuts Python's tail.
   - **BulletSupply** gives extra bullets.

5. Press **F** to shoot bullets. Bullets can destroy letters, items, and guardian snakes.

6. Guardian snakes move around the maze. Avoid them or use bullets to defeat them.

7. When the target sequence is completed, an escape portal will open somewhere on the map.

8. Enter the portal to escape from COMP9001 and win the game.

## Controls

- Arrow Keys: Move Python
- F: Shoot a bullet
- ESC: Open or close the pause menu
- R: Restart when the game is over or from the pause menu
- Q: Quit from the pause menu

## Development Progress

| Step | Feature |
|---:|---|
| 1 | Create a basic Pygame window |
| 2 | Render the grid |
| 3 | Draw the player snake |
| 4 | Add one-direction snake movement and FPS control |
| 5 | Add four-direction movement, keyboard control, and 180-degree turn prevention |
| 6 | Set up the basic layout and screen size |
| 7 | Add snake quantum teleport at map edges |
| 8 | Spawn an apple |
| 9 | Apple eating and snake growth |
| 10 | Add game-over checking and simple UI optimization |
| 11 | Add the game reset function |
| 12 | Split `main.py` into different modules |
| 13 | Letter apple and simple UI |
| 14 | Game win condition |
| 15 | Encapsulate apple, snake, map, and UI logic into classes |
| 16 | Add walls |
| 17 | Add multiple apples |
| 18 | Optimize respawn logic |
| 19 | Add apple system |
| 20 | Add item system |
| 21 | Display collected letters on the snake body |
| 22 | Add TailCut items that randomly remove 1-3 tail segments |
| 23 | Add UI status messages |
| 24 | Add an ASCII-based map layout |
| 25 | Add start, pause, and resume controls |
| 26 | Add enemy system, enemy snake, and enemy manager |
| 27 | Add collision detection between the player snake and enemy snakes |
| 28 | Add enemy death drops: golden apples and TailCut items |
| 29 | Add temporary invincibility after revival. It only affects enemy-snake collision, not wall or self-collision. |
| 30 | Allow enemy snakes to eat apples and TailCut items |
| 31 | Add the exit portal. The player wins by completing the target sequence and entering the portal. |
| 32 | Add the bullet system and BulletManager. Bullets can move and appear on screen, and the player can press F to shoot. |
| 33 | Optimized the code. The game now runs at 120 FPS, and shooting feels smoother, more natural, and more responsive. |
| 34 | Allow bullets to destroy apples and TailCut items |
| 35 | Allow bullets to affect enemy snakes: hitting the head or first body segment defeats the enemy, while hitting other body parts cuts the enemy from the hit point to the tail. |
| 36 | Allow bullets to hurt the player snake and -1 life |
| 37 | Add BulletSupply items that give a random number of bullets |
| 38 | Optimize spawning by using BFS to check whether grid positions are reachable |
| 39 | Add assets for floor tiles and wall tiles |
| 40 | Add assets for the player snake, enemy snake, apples, golden apple, TailCut, and BulletSupply |
| 41 | Add portal assets, question-mark apple assets, and an image loader for custom sizes |
| 42 | Fix a bug where paused time incorrectly affected game timers and caused game state issues. |
| 43 | Add responsive window scaling to prevent the game window from exceeding the screen boundary |
| 44 | Refactor the project structure to simplify the main function |
| 45 | Refactor parts of `game_controller.py` |
| 46 | Add a pause menu and update controls for pause, resume, reset, and quit |
| 47 | Add UI item introduction |
| 48 | Add the start interface, menu buttons, and mouse interaction |
| 49 | Add multi-page rules introduction screens |

## Naming Note

During development, the collectable letters were originally designed as letter apples, and the wildcard letter was originally designed as a golden apple.

Later, the apple background was removed because the standalone letter assets looked clearer in the grid. Therefore, in the current game, "letter" refers to the collectable letter item, and "wildcard letter" refers to the special golden wildcard item.

Some entries in the development progress still use the original terms "apple" and "golden apple" to reflect the development history and the internal class names used in the code.

- Current gameplay terms: letter / wildcard letter
- Development and internal terms: apple / golden apple
## Project Structure
```text
Python's Burden
├── main.py
├── settings.py
├── game_initialization.py
├── game_controller.py
├── input_events.py
├── display_manager.py
├── game_map.py
├── snake.py
├── apple.py
├── item.py
├── enemy.py
├── bullet.py
├── ui.py
├── assets_loader.py
├── README.md
└── assets/
    ├── fonts/
    └── images/
        ├── apples/
        ├── intro/
        ├── items/
        ├── portal/
        ├── snake/
        ├── tiles/
        └── ui/
```