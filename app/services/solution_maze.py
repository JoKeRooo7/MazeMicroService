from collections import deque
from models.maze_data_with_solution import MazeDataWithSolution


class BFS():
    def __init__(self, maze_data=None):
        self.maze_data = maze_data

    @property
    def maze_data(self) -> MazeDataWithSolution:
        return self.__maze_data

    @maze_data.setter
    def maze_data(self, maze_data) -> None:
        if maze_data is not None:
            self.__maze_data = maze_data


    def finding_way(self, maze_data=None):
        self.maze_data = maze_data
        start = self.maze_data.start_point
        end = self.maze_data.end_point
        rows, cols = self.maze_data.right_walls.shape
        way = deque([(start, [start])])
        visited = set()
        while way:
            (i, j), path = way.popleft()
            if (i, j) == end:
                self.maze_data.solution_coordinates = path
                return self.maze_data

            visited.add((i, j))
            directions = []

            if j + 1 < cols and self.maze_data.right_walls[i, j] == 0:
                directions.append((i, j + 1))
            
            if i + 1 < rows and self.maze_data.lower_walls[i, j] == 0:
                directions.append((i + 1, j))

            if j - 1 >= 0 and self.maze_data.right_walls[i, j - 1] == 0:
                directions.append((i, j - 1))

            if i - 1 >= 0 and self.maze_data.lower_walls[i - 1, j] == 0:
                directions.append((i - 1, j))

            for new_i, new_j in directions:
                if (new_i, new_j) not in visited:
                    way.append(((new_i, new_j), path + [(new_i, new_j)]))

        self.maze_data.solution_coordinates = None
        return self.maze_data

# import matplotlib.pyplot as plt
# def generate_maze(right_walls, lower_walls, path=None):

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
#                 # [x0, x1], [y0, y1]
#                 ax.plot([j + 1, j + 1], [i, i + 1], color='black')
#             # Рисуем нижнюю стену
#             if lower_walls[i, j] == 1:
#                 ax.plot([j, j + 1], [i + 1, i + 1], color='black')
    
#     if path:
#         for k in range(len(path) - 1):
#             x0, y0 = path[k]
#             x1, y1 = path[k + 1]
#             ax.plot([y0 + 0.5, y1 + 0.5], [x0 + 0.5, x1 + 0.5], color='red', linewidth=2)

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

# from backend.mazes.algorithms.generating.generating_maze import GeneratingMaze

# if __name__ == "__main__":
#     rows = 12
#     cols = 33
#     data = MazeDataWithSolution(rows=rows, cols=cols)
#     data.lower_walls = np.zeros((rows, cols))
#     data.right_walls = np.zeros((rows, cols))
#     # print(data)
#     labirint = GeneratingMaze(data)
#     data = labirint.create_maze()
#     print(data)
#     print("=====------result------======")
#     print(data.rows)
#     print(data.cols)
#     print(data.right_walls)
#     print(data.lower_walls)

#     start_coord = (np.random.randint(0, data.rows), np.random.randint(0, data.cols))
#     end_coord = (np.random.randint(0, data.rows), np.random.randint(0, data.cols))
#     solution = SolutionData(start_point=start_coord, end_point=end_coord, solution_coordinates=None)

#     my_class = BFS(maze_data=data, solution_data=solution)
#     my_way = my_class.finding_way()
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
#     print(f"{my_way=}")
#     print(type(my_way))  
#     print(f"{my_way.solution_coordinates=}")
#     print(type(my_way.solution_coordinates))  
#     generate_maze(data.right_walls, data.lower_walls, path=my_way.solution_coordinates)
