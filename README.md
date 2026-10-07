# Maze Escape

A browser game where you race to the exit of a randomly generated maze while an AI guard hunts you down using the shortest path.

**Play it:** https://arronPhilip.github.io/maze-escape/

## Features

- Random maze every game, with extra loops so there is always more than one route
- Adjustable grid size (10x10 to 25x25) and guard speed
- AI guard that chases you with breadth-first search (BFS)
- Optional overlay that shows the guard's route live
- Keyboard (arrows / WASD), swipe and on-screen touch controls
- Light and dark themes, responsive layout
- No frameworks, no build step: one HTML file with plain JavaScript

## How it works

- **Maze generation:** randomised depth-first search carves a perfect maze (one route between any two cells). A number of extra walls are then removed to create loops.
- **Guard AI:** each time the guard moves, BFS finds the shortest path from the guard's cell to the player's cell, and the guard steps along it. It moves every 1st, 2nd or 3rd turn depending on the speed setting.
- **Guard placement:** the guard starts off the shortest route to the exit, so it chases you instead of blocking the only way through.

## Run locally

Open `index.html` in any browser. No install needed.

## Python version

`python-version/maze_escape.py` is the original terminal version of the game (Python 3, no dependencies):

```
python python-version/maze_escape.py
```

## Built with

HTML, CSS, JavaScript (canvas). Built with help from Claude (Anthropic).

## License

MIT
