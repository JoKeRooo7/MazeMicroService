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
