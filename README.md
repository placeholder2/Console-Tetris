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

1. Go to the **[Releases](https://github.com/placeholder2/Console-Tetris/releases)** page.  
2. Download the latest `.zip` file for your system.  
3. Extract the files to any folder.  
4. Run `tetris.exe` to start playing.
