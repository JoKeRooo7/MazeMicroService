import random
import numpy as np
# from models.maze_data_with_solution import MazeDataWithSolution
from ..models.maze_data_with_solution import MazeDataWithSolution


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

    def create_maze(self, maze_data:MazeDataWithSolution=None) -> MazeDataWithSolution:
        self.maze_data = maze_data

        array_with_sets = self.__creating_an_array_with_sets()
        rows, cols = array_with_sets.shape

        for i in range(rows):
            self.__creating_right_walls(i=i, array_with_sets=array_with_sets, cols=cols)
            self.__creating_lower_walls(i=i, array_with_sets=array_with_sets, cols=cols, rows=rows)
        return self.maze_data

    def __creating_right_walls(self, i, array_with_sets, cols) -> None:
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
                        self.__replace_set(array_with_sets, i, j + 1, array_with_sets[i, j])

    def __creating_lower_walls(self, i, array_with_sets, cols, rows) -> None:
        for j in range(cols):
            need_lower_wals = random.choice([True, False])

            if need_lower_wals and \
                self.__cell_is_not_one_without_lower_border(array_with_sets, i, j):
                    self.__maze_data.lower_walls[i, j] = 1
            elif i != rows - 1:
                array_with_sets[i + 1, j] = array_with_sets[i, j]
            elif i == rows - 1:
                self.__maze_data.lower_walls[i, j] = 1
                if j != cols - 1:
                    if array_with_sets[i, j] != array_with_sets[i, j  + 1]:
                        self.__maze_data.right_walls[i, j] = 0
                    self.__replace_set(array_with_sets, i, j + 1, array_with_sets[i, j])

    def __creating_an_array_with_sets(self) -> np.ndarray:
        need_rows = self.maze_data.rows
        need_cols = self.maze_data.cols
        flat_atray = np.arange(1, need_rows * need_cols  + 1)
        new_array = flat_atray.reshape(need_rows, need_cols)
        return new_array

    def __replace_set(self, array_with_sets, i, j, value) -> None:
        j_indices = np.argwhere(array_with_sets[i, :]==array_with_sets[i, j])
        for idx_j in j_indices:
            array_with_sets[i , idx_j] = value

    
    def __cell_is_not_one_without_lower_border(self, array_with_sets, i, j) -> bool:
        j_indices = np.argwhere(array_with_sets[i, :]==array_with_sets[i, j])

        count_cell = 0
        for idx_j in j_indices:
            if self.__maze_data.lower_walls[i, idx_j] != 1:
                count_cell += 1

        if count_cell > 1:
            return True
        return False


# import matplotlib.pyplot as plt
# def generate_maze(right_walls, lower_walls):

#     rows, cols = right_walls.shape
#     fig, ax = plt.subplots()

#     ax.plot([0, cols], [0, 0], color='black')  # Верхняя граница
#     ax.plot([0, cols], [rows, rows], color='black')  # Нижняя граница
#     ax.plot([0, 0], [0, rows], color='black')  # Левая граница
#     ax.plot([cols, cols], [0, rows], color='black')  # Правая граница

#     # Рисуем внутренние стены
#     for i in range(rows):
#         for j in range(cols):
#             # Рисуем правую стену
#             if right_walls[i, j] == 1:
#                 ax.plot([j + 1, j + 1], [i, i + 1], color='black')
#             # Рисуем нижнюю стену
#             if lower_walls[i, j] == 1:
#                 ax.plot([j, j + 1], [i + 1, i + 1], color='black')

#     # Рисуем внешние границы лабиринта
#     ax.plot([0, cols], [0, 0], color='black')  # Верхняя граница
#     ax.plot([0, cols], [rows, rows], color='black')  # Нижняя граница
#     ax.plot([0, 0], [0, rows], color='black')  # Левая граница
#     ax.plot([cols, cols], [0, rows], color='black')  # Правая граница

#     ax.set_aspect('equal')
#     ax.invert_yaxis()  # Чтобы начало координат было в верхнем левом углу
#     plt.xticks([])  # Убираем метки по оси X
#     plt.yticks([])  # Убираем метки по оси Y
#     plt.show()


# if __name__ == "__main__":
#     rows = 10
#     cols = 10
#     data = MazeDataWithSolution(rows=rows, cols=cols)

#     labirint = GeneratingMaze(data)
#     data = labirint.create_maze()
#     print("=====------result------======")
#     print(data.rows)
#     print(data.cols)
#     print(data.right_walls)
#     print(data.lower_walls)
#     # labirint.maze_data.right_walls = np.array(
#     #     [[0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
#     #     [1, 1, 0, 0, 1, 0, 0, 0, 0, 1],
#     #     [0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
#     #     [1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
#     #     [0, 1, 0, 1, 0, 0, 1, 0, 1, 1],
#     #     [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
#     #     [0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
#     #     [1, 1, 0, 1, 0, 0, 0, 1, 1, 1]])
#     # labirint.maze_data.lower_walls = np.array(
#     #     [[0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
#     #     [0, 0, 1, 1, 0, 1, 1, 0, 0, 1],
#     #     [0, 1, 0, 0, 0, 0, 1, 1, 1, 0],
#     #     [0, 0, 0, 1, 1, 0, 1, 0, 1, 0],
#     #     [0, 1, 0, 1, 0, 1, 1, 1, 0, 0],
#     #     [0, 0, 1, 0, 0, 1, 1, 0, 0, 0],
#     #     [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
#     #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
#     # print(labirint.maze_data.lower_walls)    
#     # print(labirint.maze_data.lower_walls)    
#     generate_maze(data.right_walls, data.lower_walls)