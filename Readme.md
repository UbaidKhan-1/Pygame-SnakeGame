Snake Game

A Snake game built with Python and Pygame featuring multiple levels, obstacle layouts, sound effects, keyboard controls for desktop, and touch controls for mobile devices.

Features

- Classic Snake gameplay
- Multiple handcrafted levels
- Obstacle and wall collision
- Random food generation
- Gradient-colored snake
- Background music and sound effects
- Keyboard controls (WASD)
- Touch controls for mobile devices
- Screen wrap-around mechanics
- Score tracking
- Progressive level system

---

Gameplay

The objective is to eat food to increase your score and grow the snake. Every five points advances the game to the next level, introducing a new obstacle layout. The snake wraps around the edges of the screen, but colliding with a wall or with itself resets the game.

---

Controls

Desktop

Key| Action
W| Move Up
A| Move Left
S| Move Down
D| Move Right

Mobile

Use the on-screen directional buttons.

---

Project Structure

SnakeGame/
│
├── SnakeGame.py
├── snakelevels.py
│
├── Assets/
│   ├── Background_music.mp3
│   ├── EatingSound.mp3
│   ├── Dead.mp3
│   ├── Nextlevel.mp3
│   └── technology.ttf
│
└── README.md

---

Installation

Clone the repository:

git clone https://github.com/yourusername/snake-game.git
cd snake-game

Install the required dependency:

pip install pygame

Run the game:

python SnakeGame.py

---

Requirements

- Python 3.10 or later
- Pygame

---

Level Progression

Each level is unlocked after earning five additional points. Upon reaching the final level, the game cycles back to the first level.

---

Audio

The game includes:

- Background music
- Food collection sound effect
- Death sound effect
- Level completion sound effect

---

Mobile Support

The game supports touch controls and has been tested with Android Python environments such as Pydroid 3.

---

Customization

Game settings can be modified directly in "SnakeGame.py", including:

- Snake speed
- Initial snake length
- Snake color
- Grid size
- Level layouts
- Audio files
- Font
- Button dimensions

---

License

This project is licensed under the MIT License.