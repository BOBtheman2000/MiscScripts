import random
import time
import os

emoji_map = {
    'r':'\U0001F534',
    'R':'\U0001F7E5',
    'b':'\U000026AB',
    'B':'\U00002B1B',
    ' ':'  '
}

emoji_map_end = {
    'r':'\U0001F7E1',
    'R':'\U0001F7E8',
    'b':'\U000026AA',
    'B':'\U00002B1C',
    ' ':'  '
}

board_map = list('bbbbbbbbbbbb        rrrrrrrrrrrr')

board_row = ['───' for i in range(8)]
board_top = f"┌{'┬'.join(board_row)}┐"
board_mid = f"├{'┼'.join(board_row)}┤"
board_bot = f"└{'┴'.join(board_row)}┘"

def print_boardmap(board, msg, emojis):
    map_rows = [[board[i*4 + o] for o in range(4)] for i in range(8)]
    board_out = []
    board_out.append(board_top)
    rows = len(map_rows)
    for i in range(rows):
        row = map_rows[i]
        out_row = " │   │".join(emojis[tile] for tile in row)
        if i % 2 == 0:
            out_row = out_row + ' │   │'
            out_row = '│' + out_row
        else:
            out_row = out_row + ' │'
            out_row = '│   │' + out_row
        board_out.append(out_row)
        if i != rows-1:
            board_out.append(board_mid)
    board_out.append(board_bot)
    board_print = '\n'.join(board_out)
    os.system('cls')
    print(msg)
    print(board_print)


def get_pos_dir(pos, dir):
    pos_col = pos % 4
    pos_row = int(pos / 4)
    target_col = pos_col
    target_row = pos_row
    match dir:
        case 'u':
            target_row -= 1
            target_col += pos_row % 2 - 1
        case 'l':
            target_row += 1
            target_col += pos_row % 2 - 1
        case 'd':
            target_row += 1
            target_col += pos_row % 2
        case 'r':
            target_row -= 1
            target_col += pos_row % 2
    target = target_row*4 + target_col
    return target

def check_legal(board, src_piece, tgt_piece, dir):
    if min(abs(src_piece), 31) != src_piece or min(abs(tgt_piece), 31) != tgt_piece:
        return 0
    if abs((src_piece % 4) - (tgt_piece % 4)) > 2:
        return 0
    src = board[src_piece]
    tgt = board[tgt_piece]

    if src == 'r' and dir in ['l', 'd']:
        return 0
    if src == 'b' and dir in ['u', 'r']:
        return 0

    if src == ' ':
        return 0
    if tgt == ' ':
        return 1
    if tgt.lower() != src.lower():
        return -1
    return 0

def full_legal_check(board, piece, dir):
    jump = False
    target_piece = get_pos_dir(piece, dir)
    target_jump = 0
    check_mov = check_legal(board, piece, target_piece, dir)
    if check_mov == 0:
        return False, False, False, False
    if check_mov == -1:
        target_jump = get_pos_dir(target_piece, dir)
        check_jump = check_legal(board, piece, target_jump, dir)
        if check_jump != 1:
            return False, False, False, False
        jump = True
    
    return True, jump, target_piece, target_jump

def all_legal_moves(board, col, jumps):
    possible_pieces = []
    legal_moves = []
    for i in range(len(board)):
        if board[i].lower() == col:
            possible_pieces.append(i)
    for ind in possible_pieces:
        for dir in ['u', 'l', 'd', 'r']:
            legal, jump, _, _ = full_legal_check(board, ind, dir)
            if legal and (jump or not jumps):
                legal_moves.append([ind, dir])
    return legal_moves

def move_piece(board, piece, dir):
    new_board = board

    legal, jump, target_piece, target_jump = full_legal_check(board, piece, dir)

    if not legal:
        return board, False, False

    old_piece = board[piece]
    new_board[piece] = ' '
    if jump:
        if old_piece == 'r' and target_jump <= 3:
            old_piece = 'R'
        if old_piece == 'b' and target_jump >= 28:
            old_piece = 'B'
        new_board[target_jump] = old_piece
        new_board[target_piece] = ' '
    else:
        if old_piece == 'r' and target_piece <= 3:
            old_piece = 'R'
        if old_piece == 'b' and target_piece >= 28:
            old_piece = 'B'
        new_board[target_piece] = old_piece

    return new_board, jump, True

def ai(board, jumps):
    legal_moves = all_legal_moves(board, 'b', jumps)
    move = legal_moves[random.randint(0, len(legal_moves)-1)]
    if not jumps:
        legal_jumps = all_legal_moves(board, 'b', True)
        if len(legal_jumps) > 0:
            move = legal_jumps[random.randint(0, len(legal_jumps)-1)]
    return move[0], move[1], True

def player(board, jumps):
    new_move = input("")
    if len(new_move) == 0:
        print_boardmap(board, 'i am killing you', emoji_map_end)
        time.sleep(1)
        os.system('cls')
        exit()
    if len(new_move) != 3:
        return 0, '', False
    try:
        row = new_move[:1]
        col = new_move[1:-1]
        piece = (int(row)-1)*4 + int((int(col)-1)/2)
        dir = new_move[-1:]
    except ValueError:
        return 0, '', False
    return piece, dir, True

def check_game_over(board):
    if ('r' not in board and 'R' not in board) or ('b' not in board and 'B' not in board):
        return True
    return False

def end_game(player, draw):
    msg = "fuck!!!"
    if not draw:
        msg = "your lose :(" if player else "your winner :)"
    print_boardmap(board_map, msg, emoji_map_end)
    time.sleep(1)
    os.system('cls')
    exit()

game_over = False
player_turn = True
jump_turn = False
print_boardmap(board_map, 'i lied. this is checkers', emoji_map)
while not game_over:

    piece, dir = 0, ''
    legal_moves = all_legal_moves(board_map, 'r' if player_turn else 'b', jump_turn)
    if len(legal_moves) == 0:
        end_game(player_turn, True)
    if player_turn:
        piece, dir, valid = player(board_map, jump_turn)
        if [piece, dir] not in legal_moves:
            valid = False
    else:
        piece, dir, valid = ai(board_map, jump_turn)
    if not valid:
        print_boardmap(board_map, 'what the hell are you doing man', emoji_map)
        continue
    board_map, jump, legal = move_piece(board_map, piece, dir)
    if not legal:
        print_boardmap(board_map, 'nuh uh', emoji_map)
        continue
    if jump:
        jumps_available = len(all_legal_moves(board_map, 'r' if player_turn else 'b', True)) > 0
        jump_turn = jumps_available
    else:
        jump_turn = False
    if not jump_turn:
        player_turn = not player_turn

    if check_game_over(board_map):
        end_game(player_turn, False)

    pos_col = (piece % 4)*2
    pos_row = int(piece / 4)
    msg = f'{pos_row+1}{pos_col+1+pos_row%2}{dir}'

    print_boardmap(board_map, msg, emoji_map)

    if not player_turn:
        if jump_turn:
            print("check this out")
        else:
            print("ok, my turn...")

    time.sleep(0.6)
    