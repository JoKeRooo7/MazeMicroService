import os
import uvicorn
import numpy as np
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from models.maze_data_with_solution import MazeDataWithSolution
from services.create_gif import MazeGIF
from services.solution_maze import BFS
from services.generating_maze import GeneratingMaze
from settings import app_settings


scheduler = AsyncIOScheduler()
generate_maze_service = GeneratingMaze()
solution_maze_service = BFS()
gif_creation_service = MazeGIF()


async def new_maze():
    maze = MazeDataWithSolution()
    maze.rows = app_settings.MAZE_ROWS
    maze.cols = app_settings.MAZE_COLS
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
    try:
        maze = await new_maze()
    except:
        raise HTTPException(status_code=500, detail="Error when creating the maze")
    total_time = maze.step * app_settings.GIF_DELAY
    gif_creation_service.delay = app_settings.GIF_DELAY
    try:
        await gif_creation_service.create_gif(maze)
    except:
        raise HTTPException(status_code=500, detail="Error when creating the gif")
    return total_time


async def schedule_new_gif():
    total_time = await create_new_gif()
    run_time = datetime.now() + timedelta(seconds=total_time)
    scheduler.add_job(schedule_new_gif, 'date', run_date=run_time)
    print("Scheduler state:", scheduler.running)
    scheduler.print_jobs()


async def startup_event():
    scheduler.start()
    await schedule_new_gif()


@asynccontextmanager
async def lifespan(maze_app: FastAPI):
    await startup_event()
    yield


maze_app = FastAPI(
    tittle="Maze-gif",
    version="0.1.0",
    lifespan=lifespan
)


@maze_app.get("/maze")
async def get_maze_gif():
    if not os.path.exists(app_settings.gif_file_path):
        raise HTTPException(status_code=500, detail="File not found")
    return FileResponse(app_settings.gif_file_path)


if __name__ == "__main__":
    uvicorn.run(
        maze_app, 
        host=app_settings.APP_HOST, 
        port=app_settings.APP_PORT)