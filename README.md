# Python's Burden: Escape from COMP9001

USYD COMP9001 Final Project

## Overview

**Python's Burden: Escape from COMP9001** is a Pygame-based snake game. The player controls a snake, collects letter apples to complete a target sequence, avoids walls and enemy snakes, and uses TailCut items to remove unwanted letters from the snake body.

## Development Progress

| Step | Feature |
|---:|---|
| 1 | Basic Pygame window |
| 2 | Grid rendering |
| 3 | Draw snake |
| 4 | Snake movement in one direction and FPS control |
| 5 | Four-direction movement, keyboard control, and no 180-degree turn |
| 6 | Basic layout and screen size |
| 7 | Snake quantum transit |
| 8 | Spawn an apple |
| 9 | Apple eating and snake growth |
| 10 | Game over check and simple UI optimization |
| 11 | Reset game function |
| 12 | Divide `main.py` into different parts |
| 13 | Letter apple and simple UI |
| 14 | Game win condition |
| 15 | Encapsulate apple, snake, map, and UI into classes |
| 16 | Add walls |
| 17 | Add multiple apples |
| 18 | Optimize respawn logic |
| 19 | Add apple system |
| 20 | Add item system |
| 21 | Show letters on the snake body |
| 22 | TailCut items cut 1-3 tails randomly |
| 23 | Add UI status messages |
| 24 | Add ASCII map |
| 25 | Add start, pause, and resume controls |
| 26 | Add enemy system, enemy snake, and enemy manager |
| 27 | Add collision judgment with enemy snake |
| 28 | Add drops when enemy snake dies: golden apple and TailCut item |
| 29 | Add snake invincibility after reviving.(has no effect on self-collision or wall-collision, only applies to enemy snake collision) |
| 30 | Add enemy snake can eat apple and tailcut item now |
| 31 | Add exit portal. Now the win condition is: player collects right sequence and enters the portal |
| 32 | Add bullet system, bullet manager, now bullet move normally and are shown on the screen, but no effect. Press F to fire a bullet|
| 33 | Optimized the code. The game now runs at 60 FPS, and shooting feels smoother, more natural, and more responsive. |
| 34 | Add bullet can destroy apple, tailcut item now |
| 35 | Add bullet can kill the enemy snake, hit the head or the first segment of the body can kill the snake, hit the rest of the body can cut the body|
## Project Structure

```text
Python's Burden
├── main.py
├── settings.py
├── snake.py
├── apple.py
├── item.py
├── enemy.py
├── game_map.py
├── events.py
└── ui.py
```

## File Responsibilities

### `main.py`

`main.py` is the main control file of the game. It initializes the game, creates the main objects, runs the game loop, updates game logic, handles collisions, and draws everything on the screen.

```text
main.py
├── reset_game(game_map, ui)
│   ├── Create occupied_positions
│   ├── Create player snake
│   ├── Create apple manager
│   ├── Create item manager
│   ├── Create enemy manager
│   ├── Reset collected letters
│   ├── Reset game_over / game_win
│   ├── Reset game_started / game_paused
│   └── Reset UI status messages
│
└── main()
    ├── Initialize pygame
    ├── Create screen and clock
    ├── Create game map
    ├── Create UI and fonts
    ├── Call reset_game()
    ├── Main game loop
    │   ├── Handle keyboard events
    │   ├── Restart game if requested
    │   ├── Update apples
    │   ├── Calculate player's next head position
    │   ├── Check apple / TailCut / wall / self / enemy collisions
    │   ├── Update enemy snakes
    │   ├── Handle enemy drops
    │   ├── Move player snake normally
    │   └── Check win condition
    └── Draw map, snake, apples, items, enemies, and UI
```

### `settings.py`

`settings.py` stores global constants used by the whole game.

```text
settings.py
├── Grid settings
├── Colour settings
├── Layout settings
├── Target sequence
├── Snake settings
├── Apple settings
└── Enemy snake settings
```

### `snake.py`

`snake.py` contains the player snake class. It manages the player's body, movement, lives, revival, tail cutting, and drawing letters on the snake body.

```text
snake.py
└── class Snake
    ├── __init__(occupied_positions)
    ├── move(next_head, should_grow)
    ├── get_next_head_pos()
    ├── quantum_transit(position)
    ├── check_self_collision(next_head, apple_eaten)
    ├── lose_life()
    ├── is_dead()
    ├── create_respawn_body(length)
    ├── revive()
    ├── reset()
    ├── cut_tail(cut_count)
    └── draw(screen, font, collected_letters)
```

### `apple.py`

`apple.py` contains the apple system. It includes normal apples, golden apples, apple spawning, apple expiration, apple eating, and target sequence checking.

```text
apple.py
├── class Apple
│   ├── __init__(game_map, letter, occupied_positions)
│   ├── spawn_and_get_apple_position(game_map, occupied_positions)
│   ├── draw(screen, font)
│   ├── check_apple_eaten(next_head)
│   ├── get_random_lifetime()
│   └── is_expired()
│
├── class GoldenApple(Apple)
│   ├── __init__(pos, letter)
│   └── draw(screen, font)
│
├── class AppleManager
│   ├── __init__(game_map, collected_letters, occupied_positions, max_apples)
│   ├── get_next_required_letter(collected_letters)
│   ├── spawn_one_apple(game_map, letter)
│   ├── spawn_apples(game_map, collected_letters)
│   ├── spawn_golden_apple(pos, collected_letters)
│   ├── has_correct_letter(correct_letter)
│   ├── remove_expired_apples()
│   ├── refill_apples(game_map, collected_letters)
│   ├── update(game_map, collected_letters)
│   ├── get_eaten_apple(next_head)
│   ├── handle_apple_eaten(eaten_apple, game_map, collected_letters)
│   └── draw(screen, font)
│
├── check_target_completed(collected_letters)
└── get_random_apple_letter()
```

### `item.py`

`item.py` contains the item system. Currently, it mainly manages TailCut items.

```text
item.py
├── class TailCutItem
│   ├── __init__(game_map, occupied_positions, pos=None)
│   ├── spawn_and_get_position(game_map, occupied_positions)
│   ├── draw(screen, font)
│   └── check_item_eaten(next_head)
│
└── class ItemManager
    ├── __init__(game_map, occupied_positions)
    ├── spawn_tail_cut(game_map)
    ├── spawn_tail_cut_at_position(game_map, pos)
    ├── get_eaten_tail_cut(next_head)
    ├── handle_tail_cut_eaten(eaten_tail_cut_item, player_snake, collected_letters)
    └── draw(screen, font)
```

### `enemy.py`

`enemy.py` contains the AI snake system. It includes individual enemy snakes and the manager that controls all enemy snakes.

```text
enemy.py
├── class EnemySnake
│   ├── __init__(game_map, occupied_positions)
│   ├── spawn_and_get_body(game_map)
│   ├── draw(screen)
│   ├── get_next_head_pos(direction)
│   ├── turn_left(direction)
│   ├── turn_right(direction)
│   ├── can_move_to(game_map, pos)
│   ├── choose_direction(game_map)
│   ├── move(game_map)
│   ├── die()
│   └── quantum_transit(position)
│
└── class EnemyManager
    ├── __init__(occupied_positions)
    ├── spawn_enemy_snake(game_map)
    ├── check_player_collision(player_next_head)
    ├── handle_enemy_drops(game_map, apple_manager, item_manager, collected_letters, ui)
    ├── update(game_map)
    └── draw(screen)
```

#### How Enemy Snakes Are Removed

```text
EnemySnake.move()
    ↓
If the enemy snake has no valid direction
    ↓
EnemySnake.die()
    ↓
alive becomes False
    ↓
EnemySnake removes its body positions from occupied_positions
    ↓
EnemyManager.update()
    ↓
EnemyManager only keeps enemy snakes where alive == True
    ↓
Dead enemy snakes are not added to alive_enemies
    ↓
self.enemy_snakes = alive_enemies
```

The dead enemy snake is removed by rebuilding the `enemy_snakes` list with only alive enemies.

### `events.py`

`events.py` handles keyboard and window events.

```text
events.py
└── handle_events(game_running, direction, game_over, game_started, game_paused, ui)
    ├── Handle pygame.QUIT
    ├── SPACE starts the game
    ├── P pauses or resumes the game
    ├── R restarts the game when game over or game win
    ├── Arrow keys change player snake direction
    └── Prevent multiple direction changes in one frame
```

### `game_map.py`

`game_map.py` manages the map grid, walls, drawing, and spawn availability.

```text
game_map.py
├── Cell type constants
│   ├── EMPTY
│   ├── WALL
│   ├── OBSTACLE
│   ├── PORTAL
│   └── EXIT
│
└── class GameMap
    ├── __init__()
    ├── create_empty_grid()
    ├── create_walls()
    ├── draw(screen)
    ├── is_inside_map(pos)
    ├── get_grid(pos)
    ├── set_grid(pos, cell_type)
    ├── is_walkable(pos)
    └── is_available_for_spawn(pos, occupied_positions)
```

### `ui.py`

`ui.py` manages the right-side UI panel, control instructions, target sequence display, collected letters display, and status messages.

```text
ui.py
└── class UI
    ├── __init__(font)
    ├── add_status_message(message)
    ├── reset_status_messages()
    ├── draw(screen, lives, game_over, game_win, collected_letters)
    ├── draw_background(screen)
    ├── draw_title(screen)
    ├── draw_controls(screen)
    ├── draw_lives(screen, lives)
    ├── draw_target_sequence(screen)
    ├── draw_collected_letters(screen, collected_letters)
    └── draw_status_messages(screen)
```

## Important Notes

### Shared `occupied_positions`

Most game objects share the same `occupied_positions` list.

```text
occupied_positions
├── player snake body positions
├── apple positions
├── golden apple positions
├── TailCut item positions
└── enemy snake body positions
```

Each class is responsible for updating the shared list when its own objects are created, moved, eaten, removed, or killed.

### Player Snake Length Rule

```text
Player snake length = collected letters length + 1
```

The head does not display a letter. Each body segment displays one collected letter.

### Enemy Death Drop Rule

```text
Enemy snake dies
├── Golden apple spawns at enemy head position
└── TailCut item spawns at enemy tail position
```

### Game State

```text
game_started = False
    → waiting for SPACE

game_started = True and game_paused = False
    → game is running

game_paused = True
    → game logic stops

game_over = True
    → player can press R to restart

game_win = True
    → player can press R to restart
```
