import random
import numpy as np
from models.maze_data_with_solution import MazeDataWithSolution


class GeneratingMaze():
    def __init__(self, maze_data:MazeDataWithSolution=None):
        self.maze_data = maze_data

    @property
    def maze_data(self) -> MazeDataWithSolution:
        return self.__maze_data

    @maze_data.setter
    def maze_data(self, maze_data) -> None:   
        if maze_data is not None:
            self.__maze_data = maze_data
            self.__maze_data.right_walls = np.zeros(
                (self.__maze_data.rows, self.__maze_data.cols), 
                 dtype=int)
            self.__maze_data.lower_walls = np.zeros(
                (self.__maze_data.rows, self.__maze_data.cols), 
                 dtype=int)

    async def create_maze(self, maze_data:MazeDataWithSolution=None) -> MazeDataWithSolution:
        self.maze_data = maze_data

        array_with_sets = await self.__creating_an_array_with_sets()
        rows, cols = array_with_sets.shape

        for i in range(rows):
            await self.__creating_right_walls(i=i, array_with_sets=array_with_sets, cols=cols)
            await self.__creating_lower_walls(i=i, array_with_sets=array_with_sets, cols=cols, rows=rows)
        return self.maze_data

    async def __creating_right_walls(self, i, array_with_sets, cols) -> None:
        for j in range(cols):
            if j == cols - 1:
                self.__maze_data.right_walls[i, j] = 1
            else:
                need_right_wals = random.choice([True, False])
                if need_right_wals:
                        self.__maze_data.right_walls[i, j] = 1
                else:
                    if array_with_sets[i, j] == array_with_sets[i, j + 1]:
                        self.__maze_data.right_walls[i, j] = 1
                    else:
                        await self.__replace_set(array_with_sets, i, j + 1, array_with_sets[i, j])

    async def __creating_lower_walls(self, i, array_with_sets, cols, rows) -> None:
        for j in range(cols):
            need_lower_wals = random.choice([True, False])

            if need_lower_wals and \
                await self.__cell_is_not_one_without_lower_border(array_with_sets, i, j):
                    self.__maze_data.lower_walls[i, j] = 1
            elif i != rows - 1:
                array_with_sets[i + 1, j] = array_with_sets[i, j]
            elif i == rows - 1:
                self.__maze_data.lower_walls[i, j] = 1
                if j != cols - 1:
                    if array_with_sets[i, j] != array_with_sets[i, j  + 1]:
                        self.__maze_data.right_walls[i, j] = 0
                    await self.__replace_set(array_with_sets, i, j + 1, array_with_sets[i, j])

    async def __creating_an_array_with_sets(self) -> np.ndarray:
        need_rows = self.maze_data.rows
        need_cols = self.maze_data.cols
        flat_atray = np.arange(1, need_rows * need_cols  + 1)
        new_array = flat_atray.reshape(need_rows, need_cols)
        return new_array

    async def __replace_set(self, array_with_sets, i, j, value) -> None:
        j_indices = np.argwhere(array_with_sets[i, :]==array_with_sets[i, j])
        for idx_j in j_indices:
            array_with_sets[i , idx_j] = value

    
    async def __cell_is_not_one_without_lower_border(self, array_with_sets, i, j) -> bool:
        j_indices = np.argwhere(array_with_sets[i, :]==array_with_sets[i, j])

        count_cell = 0
        for idx_j in j_indices:
            if self.__maze_data.lower_walls[i, idx_j] != 1:
                count_cell += 1

        if count_cell > 1:
            return True
        return False

