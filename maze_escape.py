"""Maze Escape: reach the exit before the AI guard catches you.

Features:
  - Variable grid size (chosen by the player)
  - Simple AI opponent (guard that chases you using BFS shortest path)

Controls: W/A/S/D then Enter (or Q to quit).
"""

import random
from collections import deque

WALL, PATH = "#", " "
MOVES = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}


def ask_size():
    """Ask for a grid size between 10 and 25, re-prompting until valid."""
    while True:
        raw = input("Grid size (10-25): ").strip()
        if raw.isdigit() and 10 <= int(raw) <= 25:
            n = int(raw)
            return n if n % 2 == 1 else n + 1  # maze needs an odd size
        print("Please enter a whole number from 10 to 25.")


def generate_maze(n):
    """Randomised depth-first search: always produces a solvable maze."""
    maze = [[WALL] * n for _ in range(n)]
    maze[1][1] = PATH
    stack = [(1, 1)]
    while stack:
        r, c = stack[-1]
        options = []
        for dr, dc in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            nr, nc = r + dr, c + dc
            if 0 < nr < n - 1 and 0 < nc < n - 1 and maze[nr][nc] == WALL:
                options.append((nr, nc, dr, dc))
        if options:
            nr, nc, dr, dc = random.choice(options)
            maze[r + dr // 2][c + dc // 2] = PATH  # knock down wall between
            maze[nr][nc] = PATH
            stack.append((nr, nc))
        else:
            stack.pop()
    # knock down a few extra walls to create loops (more than one route)
    for _ in range(n * n // 4):
        r, c = random.randrange(1, n - 1), random.randrange(1, n - 1)
        if maze[r][c] == WALL and (
                (maze[r - 1][c] == PATH and maze[r + 1][c] == PATH) or
                (maze[r][c - 1] == PATH and maze[r][c + 1] == PATH)):
            maze[r][c] = PATH
    return maze


def bfs_next_step(maze, start, target):
    """Return the next cell on the shortest path from start to target."""
    n = len(maze)
    queue = deque([start])
    came_from = {start: None}
    while queue:
        cur = queue.popleft()
        if cur == target:
            break
        for dr, dc in MOVES.values():
            nxt = (cur[0] + dr, cur[1] + dc)
            if 0 <= nxt[0] < n and 0 <= nxt[1] < n \
                    and maze[nxt[0]][nxt[1]] == PATH and nxt not in came_from:
                came_from[nxt] = cur
                queue.append(nxt)
    if target not in came_from:
        return start
    step = target
    while came_from[step] != start and came_from[step] is not None:
        step = came_from[step]
    return step


def distance_map(maze, start):
    """BFS distances from start to every reachable cell."""
    n = len(maze)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        for dr, dc in MOVES.values():
            nxt = (cur[0] + dr, cur[1] + dc)
            if 0 <= nxt[0] < n and 0 <= nxt[1] < n \
                    and maze[nxt[0]][nxt[1]] == PATH and nxt not in dist:
                dist[nxt] = dist[cur] + 1
                queue.append(nxt)
    return dist


def place_guard(maze, player, exit_):
    """Put the guard OFF the shortest route to the exit, far from the player,
    so it has to chase you rather than block the only way through."""
    dist = distance_map(maze, player)
    route = {exit_}
    cur = exit_
    while cur != player:  # walk back along the shortest route
        cur = min(((cur[0] + dr, cur[1] + dc) for dr, dc in MOVES.values()
                   if (cur[0] + dr, cur[1] + dc) in dist),
                  key=lambda x: dist[x])
        route.add(cur)
    far = dist[exit_] // 2
    candidates = [c for c, d in dist.items() if c not in route and d >= far]
    if not candidates:
        candidates = [c for c in dist if c not in route]
    return random.choice(candidates) if candidates else exit_


def draw(maze, player, guard, exit_):
    print()
    for r, row in enumerate(maze):
        line = ""
        for c, cell in enumerate(row):
            if (r, c) == player:
                line += "P "
            elif (r, c) == guard:
                line += "G "
            elif (r, c) == exit_:
                line += "E "
            else:
                line += (cell * 2) if cell == WALL else "  "
        print(line)
    print("P = you, G = guard, E = exit")


def play():
    n = ask_size()
    maze = generate_maze(n)
    player, exit_ = (1, 1), (n - 2, n - 2)
    guard = place_guard(maze, player, exit_)
    turn = 0

    while True:
        draw(maze, player, guard, exit_)
        move = input("Move (WASD, Q to quit): ").strip().lower()
        if move == "q":
            print("Bye!")
            return
        if move not in MOVES:
            print("Use W, A, S or D.")
            continue
        dr, dc = MOVES[move]
        new = (player[0] + dr, player[1] + dc)
        if maze[new[0]][new[1]] == WALL:
            print("That's a wall!")
            continue
        player = new
        if player == exit_:
            draw(maze, player, guard, exit_)
            print("You escaped! You win!")
            return
        if player == guard:
            print("You walked into the guard. You lose!")
            return

        turn += 1
        if turn % 2 == 0:  # guard moves every other turn so you can win
            guard = bfs_next_step(maze, guard, player)
            if guard == player:
                draw(maze, player, guard, exit_)
                print("The guard caught you. You lose!")
                return


if __name__ == "__main__":
    play()
