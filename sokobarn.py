import msvcrt as m
import os
from sys import argv

chars = ['  ', '██', '■ ', '☺ ', '☻ ', '□ ', '▣ ',]
imp_map = {
    ' ':0,
    '#':1,
    '.':2,
    '@':3,
    '+':4,
    '$':5,
    '*':6
}

title = ''
grid = []
history = []

def clear_board(size:int):
    # os.system('cls')
    # breaks in powershell i think
    for i in range(size):
        print('\033[1A', end='\x1b[2K')

def print_grid():
    puz_disp = '\n'.join([''.join([chars[i] for i in line]) for line in grid])
    print(title + '\n' + puz_disp)
    return len(grid)

def get_input():
    kp = m.getch()
    # arrow key
    if kp == b'\x00' or kp == b'\xe0':
        dr = m.getch()
        match dr:
            case b'H':
                return 'up'
            case b'P':
                return 'down'
            case b'K':
                return 'left'
            case b'M':
                return 'right'
    match kp:
        case b'r':
            return 'reset'
        case b'\x08' | b'e':
            return 'undo'
        case b'n':
            return 'next'
        case b'p':
            return 'prev'
        case b'g':
            return 'goto'
    return 'exit'

def get_p_coords():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in [3, 4]:
                return x, y

def check_move(p_x, p_y, ch_x, ch_y):
    if grid[ch_y][ch_x] == 1:
        return False
    if grid[ch_y][ch_x] in [0, 2]:
        return True
    if grid[ch_y][ch_x] in [5, 6]:
        chh_x = ch_x + (ch_x - p_x)
        chh_y = ch_y + (ch_y - p_y)
        if grid[chh_y][chh_x] in [1, 5, 6]:
            return False
        if grid[chh_y][chh_x] in [0, 2]:
            return True
    print('bug')
    return True

def p_mov(dr:str):
    psh = False
    p_x, p_y = get_p_coords()
    ch_x, ch_y = p_x, p_y
    match dr:
        case 'up':
            ch_y -= 1
        case 'down':
            ch_y += 1
        case 'left':
            ch_x -= 1
        case 'right':
            ch_x += 1
    if check_move(p_x, p_y, ch_x, ch_y):
        chh_x = ch_x + (ch_x - p_x)
        chh_y = ch_y + (ch_y - p_y)

        if grid[ch_y][ch_x] == 5:
            if grid[chh_y][chh_x] == 0:
                grid[chh_y][chh_x] = 5
            if grid[chh_y][chh_x] == 2:
                grid[chh_y][chh_x] = 6
            grid[ch_y][ch_x] = 3
            psh = True
        elif grid[ch_y][ch_x] == 6:
            if grid[chh_y][chh_x] == 0:
                grid[chh_y][chh_x] = 5
            if grid[chh_y][chh_x] == 2:
                grid[chh_y][chh_x] = 6
            grid[ch_y][ch_x] = 4
            psh = True
        elif grid[ch_y][ch_x] == 2:
            grid[ch_y][ch_x] = 4
        else:
            grid[ch_y][ch_x] = 3
            
        if grid[p_y][p_x] == 3:
            grid[p_y][p_x] = 0
        if grid[p_y][p_x] == 4:
            grid[p_y][p_x] = 2
        
        history.append((dr, psh))
        return True
    return False

def p_undo():
    dr, psh = history.pop()
    p_x, p_y = get_p_coords()
    ch_x, ch_y = p_x, p_y
    match dr:
        case 'up':
            ch_y += 1
        case 'down':
            ch_y -= 1
        case 'left':
            ch_x += 1
        case 'right':
            ch_x -= 1
    chh_x = p_x + (p_x - ch_x)
    chh_y = p_y + (p_y - ch_y)
    
    if grid[ch_y][ch_x] == 2:
        grid[ch_y][ch_x] = 4
    if grid[ch_y][ch_x] == 0:
        grid[ch_y][ch_x] = 3
    
    if psh:
        if grid[p_y][p_x] == 4:
            grid[p_y][p_x] = 6
        if grid[p_y][p_x] == 3:
            grid[p_y][p_x] = 5
        
        if grid[chh_y][chh_x] == 6:
            grid[chh_y][chh_x] = 2
        if grid[chh_y][chh_x] == 5:
            grid[chh_y][chh_x] = 0
    else:
        if grid[p_y][p_x] == 4:
            grid[p_y][p_x] = 2
        if grid[p_y][p_x] == 3:
            grid[p_y][p_x] = 0

def check_clear():
    for line in grid:
        if 5 in line or 2 in line:
            return False
    return True


imp_test = ''

file = 'Microban.txt'
if len(argv) > 1:
    file = argv[1]

with open(os.path.realpath(__file__) + '\..\\' + file, 'r') as fl:
    imp_test = ''.join(fl.readlines())

puzzles = [puz.split('\n\n')[:2] for puz in imp_test.split('; ')[1:]]

def load_puzzle(ind:int):
    puz = puzzles[ind]
    grid.clear()
    for line in puz[1].split('\n'):
        gridline = []
        for item in line:
            gridline.append(imp_map[item])
        grid.append(gridline.copy())
    return puz[0]

os.system('cls')

inp = ''
curr_puzz = 0
moves = 0
title = load_puzzle(curr_puzz)
clear_size = 0
while inp != 'exit':
    clear_board(clear_size + 2)
    clear_size = print_grid()
    print(moves)
    clr = check_clear()
    if clr:
        print('clear')
        clear_size += 1
    inp = get_input()
    if inp in ['up', 'down', 'left', 'right']:
        if p_mov(inp):
            moves += 1
        continue
    if inp == 'undo':
        p_undo()
        moves -= 1
        continue
    if inp == 'exit':
        os.system('cls')
        continue
    if inp == 'next':
        curr_puzz += 1
    if inp == 'prev':
        curr_puzz -= 1
    if inp == 'goto':
        curr_puzz = int(input('goto: ')) - 1
        clear_size += 1
    title = load_puzzle(curr_puzz)
    moves = 0