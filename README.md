# Python Console Tetris 

A simple Tetris game for the console using Python's `curses` library.  
Works on **Windows**, **Linux**, and **macOS** (with native curses).

## Features
- Classic 7 Tetris shapes
- Rotation support
- Level progression with speed increase
- Score tracking
- End game screen

---
## Instructions

| Key  | Action           |
|------|------------------|
| **W** | Rotate piece     |
| **A** | Move left        |
| **S** | Move down faster |
| **D** | Move right       |
| **Q** | Quit game        |

## Scoring

| Event                          | Points / Effect                                      |
|--------------------------------|------------------------------------------------------|
| Tetromino placed               | +1 point                                             |
| Line cleared                   | +10 points                                           |
| Every 2 lines cleared         | Speed increases (up to a limit)                      |
| Pieces reach the top of board  | Game over                                            |


## Installation

### Clone the repo
```bash
git clone https://github.com/placeholder2/Console-Tetris.git
cd Console-Tetris
