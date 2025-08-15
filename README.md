# DOOM-style Raycasting Shooter 

A simple, retro 3D shooter built with Python and Pygame, inspired by classic games like DOOM. Navigate a maze, shoot moving targets, and try to get the highest score before the 2-minute timer runs out\!

-----

## Features

  * **Pseudo-3D Graphics**: Uses a Raycasting engine to create a 3D-like environment from a 2D map.
  * **Dynamic Gameplay**: Hunt down moving targets that navigate the map on their own.
  * **UI & HUD**: Includes a Heads-Up Display for Score, remaining Ammo, and a countdown Timer.
  * **Game Loop**: A complete game experience with a start, a timed challenge, and a game-over screen with your final score.
  * **Modular Code**: The project is cleanly organized into separate files for easy understanding and modification.

-----

## Project Structure

The code is split into several modules to keep things organized:

  * `main.py`: The main entry point that runs the game loop and handles game states.
  * `config.py`: Contains all the global constants and settings like screen dimensions, colors, and game rules.
  * `player.py`: Defines the `Player` class, which handles all player movement, rotation, and collision.
  * `weapon.py`: Defines the `Weapon` class, responsible for the shooting animation and ammo management.
  * `sprite.py`: Defines the `Sprite` class for the moving targets, including their AI and rendering logic.
  * `drawing.py`: Handles all the rendering logic, including the raycasting algorithm and drawing the scene.

-----

## How to Run

1.  **Prerequisites**: Make sure you have Python 3 installed.

2.  **Clone the repository**:

    ```bash
    git clone https://github.com/alakhsharma22/Simple-doom-shooter-implementation.git
    cd Simple-doom-shooter-implementation
    ```

3.  **Install dependencies**: The only library needed is Pygame.

    ```bash
    pip install pygame
    ```

4.  **Run the game**:

    ```bash
    python main.py
    ```

-----

## Future Improvements

This project has a lot of potential\! Here are a few ideas for taking it to the next level:

  * **Wall Textures**: Replace the solid-colored walls with image textures for a more immersive look.
  * **More Levels**: Implement a system to load different maps from text files instead of having one hardcoded map.
  * **Smarter Enemies**: Give the targets more advanced AI. They could chase the player, run away, or even shoot back\!
  * **Additional Weapons**: Add new weapons like a shotgun or a rapid-fire gun, each with different properties.
  * **Sound Effects & Music**: Add background music, weapon sounds, and sound effects for hitting targets to enhance the experience.
  * **Power-ups**: Introduce collectible items like health packs, ammo clips, or temporary speed boosts.
  * **Main Menu**: Create a proper main menu with options to start the game, view high scores, or exit.
