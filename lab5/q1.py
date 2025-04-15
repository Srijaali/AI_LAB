import copy

vals = {
    'P': 1, 'p': -1,
    'N': 3, 'n': -3,
    'B': 3, 'b': -3,
    'R': 5, 'r': -5,
    'Q': 9, 'q': -9,
    'K': 10, 'k': -10
}

def fen_to_board(fen):
    board = []
    rows = fen.split()[0].split('/')
    for row in rows:
        b_row = []
        for ch in row:
            if ch.isdigit():
                b_row.extend(['.'] * int(ch))
            else:
                b_row.append(ch)
        board.append(b_row)
    return board

def evaluate_board(board):
    score = 0
    for row in board:
        for piece in row:
            score += vals.get(piece, 0)
    return score

def move_to_str(i1, j1, i2, j2):
    return f"{chr(j1 + 97)}{8 - i1}{chr(j2 + 97)}{8 - i2}"

def generate_moves(board, white=True):
    directions = {
        'P': [(-1, 0)], 'p': [(1, 0)],
        'N': [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)],
        'B': [(-1,-1), (-1,1), (1,-1), (1,1)],
        'R': [(-1,0), (1,0), (0,-1), (0,1)],
        'Q': [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1)],
        'K': [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    }

    moves = []
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece == '.' or (piece.isupper() != white):
                continue
            piece_type = piece.upper()
            dirs = directions.get(piece_type, [])
            slide = piece_type in ['B', 'R', 'Q']

            for d in dirs:
                for step in range(1, 8):
                    ni, nj = i + d[0]*step, j + d[1]*step
                    if not (0 <= ni < 8 and 0 <= nj < 8):
                        break
                    target = board[ni][nj]
                    if target == '.' or target.isupper() != white:
                        new_board = copy.deepcopy(board)
                        new_board[ni][nj] = piece
                        new_board[i][j] = '.'
                        move_str = move_to_str(i, j, ni, nj)
                        moves.append((move_str, new_board))
                        if target != '.':
                            break
                    else:
                        break
                    if not slide:
                        break
    return moves

def beam_search(board, beam_width, depth_limit, white=True):
    beam = [([], board)]
    for depth in range(depth_limit):
        candidates = []
        for path, b in beam:
            moves = generate_moves(b, white)
            for move_str, new_board in moves:
                eval_score = evaluate_board(new_board)
                candidates.append((path + [move_str], new_board, eval_score))
        candidates.sort(key=lambda x: x[2], reverse=white)
        beam = [(path, b) for path, b, _ in candidates[:beam_width]]
        white = not white
    best_path, best_board = beam[0]
    return best_path, evaluate_board(best_board)
#fen used to create a chess board
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
board = fen_to_board(fen)
beam_width = 3
depth_limit = 2

best_sequence, final_score = beam_search(board, beam_width, depth_limit, white=True)

print("Best move seq:", best_sequence)
print("score:", final_score)
