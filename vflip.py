import msvcrt as m
import random as r
from os import system

# ×2s, ×3s, Voltorb, Coins
stage_data = [
    [
	    (3, 1, 6, 24),
	    (0, 3, 6, 27),
	    (5, 0, 6, 32),
	    (2, 2, 6, 36),
	    (4, 1, 6, 48),
    ],
    [
	    (1, 3, 7, 54),
	    (6, 0, 7, 64),
	    (3, 2, 7, 72),
	    (0, 4, 7, 81),
	    (5, 1, 7, 96),
    ],
    [
	    (2, 3, 8, 108),
    	(7, 0, 8, 128),
    	(4, 2, 8, 144),
    	(1, 4, 8, 162),
    	(6, 1, 8, 192),
    ],
    [
	    (3, 3, 8, 216),
    	(0, 5, 8, 243),
    	(8, 0, 10, 256),
    	(5, 2, 10, 288),
    	(2, 4, 10, 324),
    ],
    [
	    (7, 1, 10, 384),
    	(4, 3, 10, 432),
    	(1, 5, 10, 486),
    	(9, 0, 10, 512),
    	(6, 2, 10, 576),
    ],
    [
	    (3, 4, 10, 648),
    	(0, 6, 10, 729),
    	(8, 1, 10, 768),
    	(5, 3, 10, 864),
    	(2, 5, 10, 972),
    ],
    [
	    (7, 2, 10, 1152),
    	(4, 4, 10, 1296),
    	(1, 6, 13, 1458),
    	(9, 1, 13, 1536),
    	(6, 3, 10, 1728),
    ],
    [
	    (0, 7, 10, 2187),
    	(8, 2, 10, 2304),
    	(5, 4, 10, 2592),
    	(2, 6, 10, 2916),
    	(7, 3, 10, 3456),
    ],
]

# Helper for writing clean numbers
# Should be ok since row values won't exceed 99
def ext(value):
    if len(str(value)) > 1:
        return str(value)
    else:
        return ' ' + str(value)

class Grid():
    def __init__(self):
        self.cleanup_lines = 0
        self.selected = (0, 0)
        self.row_selection = False
        self.column_selection = False
        self.curr_level = 0
        self.score_total = 0
        self.repop_grid()

    def int_pos(self, pos):
        x = pos % 5
        y = int(pos/5)
        return x, y

    def repop_grid(self):
        data = stage_data[self.curr_level][r.randint(0, 4)]

        self.grid = [[0] * 5 for i in range(5)]
        self.revealed = [[False] * 5 for i in range(5)]
        self.notes = [[0] * 5 for i in range(5)]
        self.score = 1

        twos = data[0]
        threes = data[1]
        mines = data[2]

        point_locs = r.sample(range(25), 25 - mines)
        for pos in point_locs:
            x, y = self.int_pos(pos)
            self.grid[y][x] += 1
        
        score_locs = r.sample(point_locs, twos + threes)
        for pos in score_locs:
            x, y = self.int_pos(pos)
            self.grid[y][x] += 1
        
        three_locs = r.sample(score_locs, threes)
        for pos in three_locs:
            x, y = self.int_pos(pos)
            self.grid[y][x] += 1
        
    def print(self, buffer_clear = False):
        grid_rows = []
        column_values = [0] * 5
        column_mines = [0] * 5
        for y in range(5):
            row_value = sum(self.grid[y])
            row_mines = self.grid[y].count(0)
            row_lines = [[],[],[]]
            for x in range(5):
                grid_value = self.grid[y][x]
                column_values[x] += grid_value
                if grid_value == 0:
                    column_mines[x] += 1
                
                sel_chr_h = '  '
                sel_chr_v = '  '
                if self.selected == (x, y):
                    sel_chr_h = ' @'
                    sel_chr_v = ' @'
                if self.row_selection and self.selected[1] == y:
                    sel_chr_h = ' @'
                if self.column_selection and self.selected[0] == x:
                    sel_chr_v = ' @'
                
                note = ['  '] * 4
                cell_note = self.notes[y][x]
                if cell_note & 1:
                    note[0] = '0 '
                if cell_note & 2:
                    note[1] = ' 1'
                if cell_note & 4:
                    note[2] = '2 '
                if cell_note & 8:
                    note[3] = ' 3'

                rev_chr = '  '
                if self.revealed[y][x]:
                    rev_chr = f' {grid_value}'
                    note = ['  '] * 4

                row_lines[0].append(f"{note[0]}{sel_chr_v}{note[1]}")
                row_lines[1].append(f"{sel_chr_h}{rev_chr}{sel_chr_h}")
                row_lines[2].append(f"{note[2]}{sel_chr_v}{note[3]}")
            output = ['|'.join(line) for line in row_lines]
            output[0] += f' {row_value}'
            output[2] += f' {row_mines}'
            grid_rows.append ('\n'.join(output))
        
        grid_header = f'<{self.curr_level + 1}> {self.score_total} | {self.score}'
        grid_row_output = '\n------|------|------|------|------\n'.join(grid_rows)
        grid_footer = ' '.join([f'{ext(column_values[c])}   {column_mines[c]}' for c in range(5)])

        if buffer_clear:
            self.cleanup()
        print(f'{grid_header}\n{grid_row_output}\n{grid_footer}')
        self.cleanup_lines = len(grid_rows)*4 + 2
    
    def cleanup(self):
        for i in range(self.cleanup_lines):
            print('\033[1A', end='\x1b[2K')
    
    def refresh(self):
        self.print(True)

    def validate(self):
        for y in range(5):
            for x in range(5):
                if not self.revealed[y][x]:
                    if self.grid[y][x] > 1:
                        return False
        return True

    def reveal_all(self):
        self.revealed = [[True] * 5 for i in range(5)]

    def toggle_selection_type(self, type: str = 'na'):
        if type == 'row':
            self.row_selection = not self.row_selection
        if type == 'column':
            self.column_selection = not self.column_selection

    def move_selection(self, x, y):
        self.selected = ((self.selected[0] + x) % 5, (self.selected[1] + y) % 5)
    
    def mark_selection(self, mark: int):
        note = self.notes[self.selected[1]][self.selected[0]]
        note = note ^ (1 << mark)
        if self.row_selection:
            if self.column_selection:
                for i in range(5):
                    self.notes[i][self.selected[0]] = note
            for i in range(5):
                self.notes[self.selected[1]][i] = note
        else:
            if self.column_selection:
                for i in range(5):
                    self.notes[i][self.selected[0]] = note
            else:
                self.notes[self.selected[1]][self.selected[0]] = note
    
    def select_selection(self):
        if self.revealed[self.selected[1]][self.selected[0]] == True: return

        self.revealed[self.selected[1]][self.selected[0]] = True
        revealed_tile = self.grid[self.selected[1]][self.selected[0]]

        self.score *= revealed_tile

        # Fail
        if revealed_tile == 0:
            self.reveal_all()
            self.refresh()
            self.curr_level = max(self.curr_level - 1, 0)
            gr.repop_grid()
            if m.getch() in [b'\x00', b'\xe0']:
                m.getch()
            return
        
        # W
        if self.validate():
            self.score_total += self.score
            self.reveal_all()
            self.refresh()
            self.curr_level = min(self.curr_level + 1, 7)
            self.repop_grid()
            if m.getch() in [b'\x00', b'\xe0']:
                m.getch()

        return

def handle_input(grid: Grid):
    kp = m.getch()
    # arrow key
    if kp == b'\x00' or kp == b'\xe0' or kp in [b'w', b'a', b's', b'd']:
        if kp == b'\x00' or kp == b'\xe0':
            kp = m.getch()
        match kp:
            case b'H' | b'w':
                grid.move_selection(0, -1)
            case b'P' | b's':
                grid.move_selection(0, 1)
            case b'K' | b'a':
                grid.move_selection(-1, 0)
            case b'M' | b'd':
                grid.move_selection(1, 0)
        return
    if kp == b'r':
        grid.toggle_selection_type('row')
        return
    if kp == b'c':
        grid.toggle_selection_type('column')
        return
    if kp in [b'0', b'1', b'2', b'3']:
        grid.mark_selection(int(kp))
        return
    if kp == b'4':
        grid.mark_selection(0)
        grid.mark_selection(1)
        return
    if kp in [b' ', b'\r', b'5']:
        grid.select_selection()
        return
    exit()
    
system('cls')

gr = Grid()
gr.print()
while True:
    handle_input(gr)
    gr.refresh()

pass
# controls
# - wasd/arrow keys: move cursor
# - 0/1/2/3: mark selected tile
# - 4: mark selected tile with 0 & 1
# - space/enter/5: select tile
# - r/c: toggle row/column marking mode respectively
# - press anything when round is complete to progress
# - any invalid input exits the program