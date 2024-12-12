import os
import config
import uvicorn
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from models.maze_data_with_solution import MazeDataWithSolution
from services.create_gif import MazeGifGenerator
from services.solution_maze import BFS
from services.generating_maze import GeneratingMaze


scheduler = BackgroundScheduler()


async def new_maze():
    maze = MazeDataWithSolution()
    maze.rows = config.STD_MAZE_ROWS
    maze.cols = config.STD_MAZE_COLS
    generate_maze_service = GeneratingMaze()
    solution_maze_service = BFS()
    maze.start_point = (
        np.random.randint(0, maze.rows), 
        np.random.randint(0, maze.cols))
    maze.end_point = (
        np.random.randint(0, maze.rows), 
        np.random.randint(0, maze.cols))
    while maze.start_point == maze.end_point:
        maze.end_point = (
            np.random.randint(0, maze.rows), 
            np.random.randint(0, maze.cols)
        )
    maze = generate_maze_service.create_maze(maze)
    maze = solution_maze_service.finding_way(maze)
    maze.step = len(maze.solution_coordinates) 
    return maze


async def create_new_gif():
    maze = await new_maze()
    gif_generator = MazeGifGenerator(maze)
    gif_path = config.GIF_FILE_PATH
    total_time = gif_generator.generate_gif(gif_path)
    return total_time


async def schedule_new_gif():
    total_time = await create_new_gif()  # Получаем время для следующего запуска
    scheduler.add_job(schedule_new_gif, 'date', run_date=scheduler.now + total_time)


async def startup_event():
    await schedule_new_gif()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_event()
    yield
    # await shutdown_event()


my_app = FastAPI(
    tittle="Maze-gif",
    version="0.1.0",
    lifespan=lifespan
)

@my_app.get("/standart_maze")
async def get_maze_gif():
    if not os.path.exists(config.GIF_FILE_PATH):
        raise HTTPException(status_code=500, detail="File not found")
    return FileResponse(config.GIF_FILE_PATH)


if __name__ == "__main__":
    uvicorn.run(my_app, host="127.0.0.1", port=8000)