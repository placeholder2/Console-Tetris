import curses
import time
import random

# ====== Tetromino definitions ======
tetrominoes = [
    [[1,1,1],
     [0,1,0],
     [0,0,0]],

    [[0,2,2],
     [2,2,0],
     [0,0,0]],

    [[3,3,0],
     [0,3,3],
     [0,0,0]],

    [[4,0,0],
     [4,4,4],
     [0,0,0]],

    [[0,0,5],
     [5,5,5],
     [0,0,0]],

    [[6,6,6],
     [0,0,0],
     [0,0,0]],

    [[7,7,0],
     [7,7,0],
     [0,0,0]]
]

# ====== Display symbols and colors ======
CELL_CHARS = {
    0: "  ",   # empty space
    1: "██",   
    2: "██",
    3: "██",
    4: "██",
    5: "██",
    6: "██",
    7: "██"
}

CELL_COLORS = {
    0: 0,  # default
    1: 1,  # blue
    2: 2,  # red
    3: 3,  # green
    4: 4,  # yellow
    5: 5,  # magenta
    6: 6,  # cyan
    7: 7   # white
}

# ====== Helper functions ======
def rotate(matrix):
    return [list(row) for row in zip(*matrix[::-1])]

def can_move(board, piece, offset_x, offset_y):
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                new_x = offset_x + x
                new_y = offset_y + y
                if (new_x < 0 or new_x >= len(board[0]) or
                    new_y < 0 or new_y >= len(board) or
                    board[new_y][new_x]):
                    return False
    return True

def merge(board, piece, offset_x, offset_y):
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                board[offset_y + y][offset_x + x] = cell
                
def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared = len(board) - len(new_board)
    # Add empty rows on top for the cleared lines
    for _ in range(cleared):
        new_board.insert(0, [0]*len(board[0]))
    return new_board, cleared
                

def draw_board(win, board, piece, offset_x, offset_y, score,level,lines_cleared):
    win.erase()
    height = len(board)
    width = len(board[0])

    # Draw border
    for y in range(height + 2):
        win.addstr(y, 0, "│")
        win.addstr(y, width*2 + 1, "│")
    win.addstr(0, 0, "┌" + "─"*(width*2) + "┐")
    win.addstr(height + 1, 0, "└" + "─"*(width*2) + "┘")

    # Draw settled blocks
    for y in range(height):
        for x in range(width):
            cell = board[y][x]
            char = CELL_CHARS[cell]
            win.addstr(y+1, x*2 + 1, char, curses.color_pair(CELL_COLORS[cell]))

    # Draw falling piece
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                char = CELL_CHARS[cell]
                win.addstr(offset_y + y + 1, (offset_x + x)*2 + 1, char, curses.color_pair(CELL_COLORS[cell]))

    # Draw score
    win.addstr(1, width*2 + 4, f"Score: {score}")
    win.addstr(3, width*2 + 4, f"Lines: {lines_cleared}")
    win.addstr(4, width*2 + 4, f"Level: {level}")

    win.refresh()


def show_welcome(stdscr):
    stdscr.clear()
    stdscr.nodelay(False)  # <-- wait for key press
    h, w = stdscr.getmaxyx()

    title = "T E T R I S"
    subtitle = "Press any key to start"

    stdscr.attron(curses.A_BOLD)
    stdscr.addstr(h // 2 - 2, w // 2 - len(title) // 2, title, curses.color_pair(3))
    stdscr.attroff(curses.A_BOLD)
    stdscr.addstr(h // 2, w // 2 - len(subtitle) // 2, subtitle)
    stdscr.refresh()

    # Clear any old buffered input (e.g., Enter from starting program)
    curses.flushinp()

    # Wait for *new* key press
    while True:
        key = stdscr.getch()
        if key != -1:  # Something was pressed
            break

    stdscr.clear()
    stdscr.nodelay(True)  # Restore game speed mode
	


# ====== Main game ======
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)
    lines_cleared = 0
    level = 1
    speed = 0.5
    min_speed = 0.1
    lines_per_level = 2

    show_welcome(stdscr)
    if not curses.has_colors():
        raise RuntimeError("Terminal does not support colors")
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

    height, width = 20, 10
    board = [[0]*width for _ in range(height)]

    piece = random.choice(tetrominoes)
    piece_x, piece_y = width//2 - len(piece[0])//2, 0
    score = 0

    last_time = time.time()
    speed = 0.5

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('a'):
            if can_move(board, piece, piece_x-1, piece_y):
                piece_x -= 1
        elif key == ord('d'):
            if can_move(board, piece, piece_x+1, piece_y):
                piece_x += 1
        elif key == ord('s'):
            if can_move(board, piece, piece_x, piece_y+1):
                piece_y += 1
        elif key == ord('w'):
            rotated = rotate(piece)
            if can_move(board, rotated, piece_x, piece_y):
                piece = rotated

        if time.time() - last_time > speed:
            if can_move(board, piece, piece_x, piece_y+1):
                piece_y += 1
            else:
                merge(board, piece, piece_x, piece_y)
                board, cleared = clear_lines(board)
                lines_cleared += cleared
                if lines_cleared // lines_per_level > level - 1:
                    level += 1
                    speed = max(min_speed, speed * 0.8)
                    score += 20  # 10 point per tetromino placed
                else:
                    score += 10
                piece = random.choice(tetrominoes)
                piece_x, piece_y = width//2 - len(piece[0])//2, 0
                if not can_move(board, piece, piece_x, piece_y):
                    break
            last_time = time.time()

        draw_board(stdscr, board, piece, piece_x, piece_y, score,level,lines_cleared)

    # Game loop ends here 
    stdscr.nodelay(False)
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    end_msg = "GAME OVER"
    score_msg = f"Final Score: {score}"
    score_msg = f"Final Level: {level}"

    prompt_msg = "Press Ctrl+C to exit"

    stdscr.addstr(h//2 - 1, w//2 - len(end_msg)//2, end_msg, curses.A_BOLD | curses.color_pair(7))
    stdscr.addstr(h//2, w//2 - len(score_msg)//2, score_msg)
    stdscr.addstr(h//2 + 2, w//2 - len(prompt_msg)//2, prompt_msg, curses.A_DIM)

    stdscr.refresh()

    # Infinite wait loop:
    while True:
       time.sleep(1)
       
	


curses.wrapper(main)
