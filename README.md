# Programming-Project-1
Programming Project 1: Solving the 8-puzzle problem using A* search algorithm

## Description
This program solves the 8-puzzle problem using the A* search algorithm. The 8-puzzle is a 3x3 sliding tile puzzle where you move tiles to reach a goal configuration. The program supports two heuristics and compares their performance.

## Requirements
- Python 3.x
- No external libraries needed (only built-in `heapq`)

## How to Run
```
python Astar_8_Puzzle.py
```

## Usage
1. Enter the **initial state**: 9 numbers from 0–8 separated by spaces (0 = blank tile)
2. Enter the **goal state**: the desired final arrangement

Example input:
```
Enter initial state (9 numbers 0-8, 0 = blank): 1 2 5 3 4 0 6 7 8
Enter goal state (9 numbers 0-8, 0 = blank): 1 2 5 3 4 8 6 7 0
```

## Heuristics
- **h1 - Misplaced Tiles**: counts how many tiles are not in their goal position
- **h2 - Manhattan Distance**: sums the distance each tile needs to travel to reach its goal position

## Output
The program prints the step-by-step solution for each heuristic, along with:
- Total moves to reach the goal
- Number of nodes generated
- Number of nodes expanded

## Notes
- If the initial and goal states have different inversion parities, the puzzle is unsolvable and the program will notify you
- Manhattan Distance (h2) is generally more efficient and expands fewer nodes than Misplaced Tiles (h1)
