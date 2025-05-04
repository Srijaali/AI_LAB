import random
import string

GRID_SIZE = 10
SHIP_SIZES = [5, 4]  
def create_board():
    return [['~'] * GRID_SIZE for _ in range(GRID_SIZE)]

def print_board(board, hide_ships=False):
    print("  " + " ".join(string.ascii_uppercase[:GRID_SIZE]))
    for i, row in enumerate(board):
        display_row = []
        for cell in row:
            if hide_ships and cell == 'S':
                display_row.append('~')
            else:
                display_row.append(cell)
        print(f"{i} " + " ".join(display_row))
    print()

def is_valid_placement(board, row, col, size, horizontal):
    for i in range(size):
        r = row
        c = col + i if horizontal else col
        if r >= GRID_SIZE or c >= GRID_SIZE or board[r][c] != '~':
            return False
    return True

def place_ship(board, size):
    placed = False
    while not placed:
        horizontal = random.choice([True, False])
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - size if horizontal else GRID_SIZE - 1)
        if is_valid_placement(board, row, col, size, horizontal):
            for i in range(size):
                r = row
                c = col + i if horizontal else col
                board[r][c] = 'S'
            placed = True

def parse_coordinate(coord):
    try:
        col = string.ascii_uppercase.index(coord[0].upper())
        row = int(coord[1:])
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return row, col
    except:
        pass
    return None

def player_turn(ai_board, display_board):
    while True:
        coord = input("Enter coordinate to fire (e.g., B4): ")
        pos = parse_coordinate(coord)
        if not pos:
            print("Invalid coordinate. Try again.")
            continue
        row, col = pos
        if display_board[row][col] != '~':
            print("Already targeted. Try again.")
            continue
        if ai_board[row][col] == 'S':
            print("Hit!")
            display_board[row][col] = 'X'
            ai_board[row][col] = 'X'
        else:
            print("Miss.")
            display_board[row][col] = 'O'
        break

def ai_turn(player_board, ai_memory):
    # Hunt mode: random search or targeting neighbors
    targets = ai_memory['targets']
    if targets:
        row, col = targets.pop()
    else:
        while True:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            if player_board[row][col] in ('~', 'S'):
                break
    print(f"AI fires at {string.ascii_uppercase[col]}{row}")
    if player_board[row][col] == 'S':
        print("AI hit your ship!")
        player_board[row][col] = 'X'
        # Add adjacent cells to AI targets
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            r, c = row + dr, col + dc
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                if player_board[r][c] in ('~', 'S'):
                    ai_memory['targets'].append((r, c))
    else:
        print("AI missed.")
        player_board[row][col] = 'O'

def all_ships_sunk(board):
    return all(cell != 'S' for row in board for cell in row)

def main():
    player_board = create_board()
    ai_board = create_board()
    player_view = create_board()
    ai_memory = {'targets': []}

    print("Placing your ships randomly...")
    for size in SHIP_SIZES:
        place_ship(player_board, size)

    print("Placing AI ships...")
    for size in SHIP_SIZES:
        place_ship(ai_board, size)

    while True:
        print_board(player_view, hide_ships=False)
        player_turn(ai_board, player_view)
        if all_ships_sunk(ai_board):
            print("Congratulations!")
            break
        ai_turn(player_board, ai_memory)
        if all_ships_sunk(player_board):
            print("You lost")
            break

if __name__ == '__main__':
    main()
