'''
By Prithvi Koka and Krishna Patel
ITCS 6150-091
'''
#Import priority queue algorithm
import heapq

#Initiate a PuzzleState class 
#Stores board configuration, parent state, move token, depth, and total cost
#Cost is f(n) = g(n) + h(n)
class PuzzleState:
    def __init__(self, board, parent, move, depth, cost):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

#States with lower cost are given higher priority in the queue
    def __lt__(self, other):
        return self.cost < other.cost

#Displays the board
def print_board(board):
    print("+---+---+---+")
    for row in range(0, 9, 3):
        row_visual = "|"
        for tile in board[row:row + 3]:
            if tile == 0:  
                row_visual += "   |"
            else:
                row_visual += f" {tile} |"
        print(row_visual)
        print("+---+---+---+")


#Moves dictionary represents possible tiles the blank tile can move
moves = {
    'U': -3,  
    'D': 3,   
    'L': -1,  
    'R': 1   
}

# 1 Heuristic function calculating the number of tiles not in their goal position
# Blank is excluded so the heuristic can't overestimate number of moves remaining.
def heuristic_misplaced(board, goal_pos):
    return sum(1 for i, tile in enumerate(board)
            if tile != 0 and goal_pos[tile] != divmod(i, 3))
        

#2 Heuristic function (Manhattan Distance) which computes how far each tile is from the correct position in goal state.
#A* prioritizes tiles with less distance
def heuristic_manhattan(board, goal_pos):
    distance = 0
    for i, tile in enumerate(board):
        if tile != 0:
            x1, y1 = divmod(i, 3)
            x2, y2 = goal_pos[tile]
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

HEURISTICS = [
    ("h1: Misplaced Tiles", heuristic_misplaced),
    ("h2: Manhattan distance", heuristic_manhattan)
]


#Moves the blank tile and generates a new board configuration
def move_tile(board, move, blank_pos):
    new_board = board[:]
    new_blank_pos = blank_pos + moves[move]
    new_board[blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[blank_pos]
    return new_board


#A* function searches optimal solution
#Uses priority queue to explore states with lowest estimated cost, search continues until goal state is found
#Invalid moves are ignored (Can't move outside boundaries of 3x3)
#Start_State is the initial state of the board
def a_star(start_state, goal_state, heuristic):
    goal_pos = {tile: divmod(i,3) for i, tile in enumerate(goal_state)}
    open_list = []
    closed_list = set()
    generated = 1  #Counts nodes pushed
    expanded = 0   #Counts nodes popped/processed

    heapq.heappush(open_list, PuzzleState(start_state, None, None, 0, heuristic(start_state, goal_pos)))


    while open_list:

        #Pop current elements from state into priority queue 
        current_state = heapq.heappop(open_list)

        #Skip duplicates
        if tuple(current_state.board) in closed_list:
            continue

        #If current state is already goal, return current state
        if current_state.board == goal_state:
            return current_state, generated, expanded

        #Closed List adds current state
        closed_list.add(tuple(current_state.board))

        #Expanded
        expanded += 1

        #Find the blank index
        blank_pos = current_state.board.index(0)

        #Generate successors
        for move in moves:
            if move == 'U' and blank_pos < 3:  
                continue
            if move == 'D' and blank_pos > 5:  
                continue
            if move == 'L' and blank_pos % 3 == 0:  
                continue
            if move == 'R' and blank_pos % 3 == 2:  
                continue

            #Generate new board
            new_board = move_tile(current_state.board, move, blank_pos)

            #Checks whether the board we just generated has already been explored. Following line is path cost of successor
            if tuple(new_board) in closed_list:
                continue
            g = current_state.depth + 1

            #Pushes new board onto queue
            heapq.heappush(open_list, PuzzleState(new_board, current_state, move, g, g + heuristic(new_board, goal_pos)))

            #Add one since new board generated
            generated += 1

    return None, generated, expanded

#Print solution of board
def print_solution(solution):
    path = []
    current = solution
    while current:
        path.append(current)
        current = current.parent
    path.reverse()

    for step in path:
        if step.move is None:
            print("Initial state")
        else:
            print(f"Move {step.move}")
        print_board(step.board)

#User input function for initial state and goal state.
def read_state(prompt):
    while True:
        raw = input(f"{prompt} (9 numbers 0-8, 0 = blank): ").replace(",", " ").split()
        try:
            values = [int(x)  for x in raw]
        except ValueError:
            print(" Numbers only. Please try again.")
            continue
        if sorted(values) != list(range(9)):
            print(" Input must use exactly 0-8 once. Please try again.")
            continue
        return values

#Counts inversions and checks to see if number of inversions are even (solvable)
def inversion_parity(board):
    tiles = [t for t in board if t != 0]
    inversions = sum(1 for i in range(len(tiles))
                       for j in range(i + 1, len(tiles))
                       if tiles[i] > tiles[j])
    return inversions % 2

#Main Program:
initial_state = read_state("Enter initial state")
goal_state = read_state("Enter goal state")

print("\nInitial State:")
print_board(initial_state)

print("Goal State")
print_board(goal_state)

#Inversion Check: No solution found, goal isn't reachable
#Prints out solution with number of nodes generated, and expanded.
if inversion_parity(initial_state) != inversion_parity(goal_state):
    print("No solution exists (goal not reachable from initial state).")
else:
    for name, h in HEURISTICS:
        print(f"\n===== {name} =====")
        solution, generated, expanded = a_star(initial_state, goal_state, h)
        if solution:
            print("Solution found:")
            print_solution(solution)
            print(f"Moves:           {solution.depth}")
            print(f"Nodes generated: {generated}")
            print(f"Nodes expanded:  {expanded}")
        else:
            print("No solution exists.")


