from pathlib import Path
import os

GIF_DIRECTORY = "files"
os.makedirs(GIF_DIRECTORY, exist_ok=True)

GIF_FILE_NAME = "maze.gif"
GIF_FILE_PATH = Path(GIF_DIRECTORY) / GIF_FILE_NAME

STD_MAZE_ROWS = 35
STD_MAZE_COLS = 35
