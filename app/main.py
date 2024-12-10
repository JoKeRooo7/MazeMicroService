import numpy as np
from fastapi import FastAPI,Query
from MazeMicroservice.app.models.maze_data_with_solution import MazeDataWithSolution
from app.services.generating_maze import GeneratingMaze
from app.services.solution_maze import BFS


app = FastAPI(
    tittle="Maze",
    version="0.1.0",
    # lifespan=lifespan
)



# @app.post("/generate_maze", response_model=MazeWithDynamicSolutionData)
# def generate_maze(rows: int, cols: int):
#     maze_data = maze_generator_service.generate_maze(rows, cols)
#     return maze_data


# @app.post("/solve_maze", response_model=MazeWithDynamicSolutionData)
# def solve_maze(maze_data: MazeWithDynamicSolutionData):
#     solution = maze_solver_service.solve_maze(maze_data)
#     maze_data.solution_coordinates = solution
#     maze_data.step = len(solution)
#     maze_data.current_position = solution[-1] if solution else maze_data.start_point
#     return maze_data


@app.get("/maze/{m}x{n}/random_solve")
async def generate_and_solve(
    m: int = Query(..., ge=2, le=50, description="Количество строк в лабиринте (от 2 до 50)"),
    n: int = Query(..., ge=2, le=50, description="Количество столбцов в лабиринте (от 2 до 50)"),
    ):
    maze  = MazeDataWithSolution(
        rows=m,
        cols=n,
        start_point=(np.random.randint(0, m), np.random.randint(0, n)),
        end_point=(np.random.randint(0, m), np.random.randint(0, n)),
    )
    while maze.start_point == maze.end_point:
        maze.end_point = (np.random.randint(0, m), np.random.randint(0, n))
    maze_generator_service = GeneratingMaze()
    maze_generator_service.create_maze(maze)
    maze_solver_service = BFS()
    maze.solution_coordinates =  maze_solver_service.finding_way(maze)
    maze.step = len(maze.solution_coordinates)
    return maze


@app.get("/maze/{m}x{n}/random_solve/ready_labirint")
async def generate_and_solve()

