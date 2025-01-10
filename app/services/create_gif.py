import imageio.v2 as imageio
import matplotlib.pyplot as plt
# from settings import app_settings
# from models.maze_data_with_solution import MazeDataWithSolution
from ..settings import app_settings
from ..models.maze_data_with_solution import MazeDataWithSolution


class MazeGIF:
    def __init__(self, maze_data: MazeDataWithSolution, delay: float = 0.1):
        """
            :param maze_data: Объект MazeDataWithSolution с данными лабиринта и путём.
            :param delay: Время задержки между кадрами в секундах.
        """
        self.maze_data = maze_data
        self.delay = delay
        self.images = []  # Для хранения кадров GIF
        self.last_image = None
        self._shift = +0.5

    def _x_limit(self):
        """
            Возращает пределы координат изображения по оси x
        """
        # return 0, self.maze_data.cols
        return -0.1 * app_settings.WALL_THICKNESS, self.maze_data.cols + 0.1 * app_settings.WALL_THICKNESS

    def _y_limit(self):
        """
            Возращает пределы координат изображения по оси y
        """
        # return 0, self.maze_data.rows
        return -0.1 * app_settings.WALL_THICKNESS, self.maze_data.rows + 0.1 * app_settings.WALL_THICKNESS
    
    def _draw_base_maze(self):
        """ 
            Отрисовывает лабиринт без решения (только стены, старт и конец).
        """
        maze = self.maze_data
        plt.figure(
            figsize=(
                app_settings.IMAGE_LENGHT,
                app_settings.IMAGE_HEIGHT 
            )
        )

        for i in range(maze.rows):
            for j in range(maze.cols):
                if maze.right_walls[i, j]:
                    plt.plot(
                        [j + 1, j + 1], 
                        [i, i + 1], 
                        color=app_settings.WALL_COLOR,
                        linewidth=app_settings.WALL_THICKNESS)
                if maze.lower_walls[i, j]:
                    plt.plot(
                        [j, j + 1], 
                        [i + 1, i + 1], 
                        color=app_settings.WALL_COLOR,
                        linewidth=app_settings.WALL_THICKNESS)
                if j == 0:  # Если на первом столбце
                    plt.plot(
                        [j, j], 
                        [i, i + 1], 
                        color=app_settings.WALL_COLOR, 
                        linewidth=app_settings.WALL_THICKNESS
                    )
                if i == 0:  # Если на первом ряду
                    plt.plot(
                        [j, j + 1], 
                        [i, i], 
                        color=app_settings.WALL_COLOR, 
                        linewidth=app_settings.WALL_THICKNESS
                    )
        plt.scatter(
            maze.start_point[1] +  self._shift,
            maze.start_point[0] +  self._shift,
            color=app_settings.POINT_COLOR,
            s=app_settings.POINT_SIZE,
            marker="v",
            label="Start"
        )
        plt.scatter(
            maze.end_point[1] +  self._shift,
            maze.end_point[0] +  self._shift,
            color=app_settings.POINT_COLOR,
            s=app_settings.POINT_SIZE, 
            marker="s",
            label="End")
        min_x, max_x = self._x_limit()
        min_y, max_y = self._y_limit()
        plt.xlim(min_x ,max_x)
        plt.ylim(min_y, max_y)
        plt.axis("off")
        plt.gca().invert_yaxis()
        plt.tight_layout(pad=0)
        self.last_image = f"{app_settings.GIF_DIRECTORY}/base.png"
        plt.savefig(self.last_image, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close()

    def _draw_path_frame(self, path_segment):
        """ 
            Добавляет текущий путь на базовый фон и сохраняет кадр. 
        """
        base_image = plt.imread(self.last_image)
        plt.figure(figsize=(
            app_settings.IMAGE_LENGHT,
            app_settings.IMAGE_HEIGHT 
            )
        )
        min_x, max_x = self._x_limit()
        min_y, max_y = self._y_limit()
        plt.imshow(
            base_image, 
            extent=[
                min_x, max_x, 
                min_y, max_y
                ]
            )
        y1, x1 = path_segment[0]
        y2, x2 = path_segment[1]
        max_y = self.maze_data.rows
        max_x = self.maze_data.cols
        plt.plot(
            # [x1 + self._shift, x2 + self._shift], - without invert in _draw_base_maze
            # [y1 + self._shift , y2 + self._shift], - without invert in _draw_base_maze
            [x2 + self._shift, x1 + self._shift],
            [max_y - y2 - self._shift , max_y - y1 - self._shift],
            color=app_settings.WAY_COLOR
            )
        plt.axis("off")
        # plt.gca().invert_yaxis()
        plt.tight_layout(pad=0)
        self.last_image = f"{app_settings.GIF_DIRECTORY}/{len(self.images)}.png"
        plt.savefig(self.last_image, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close()
        self.images.append(imageio.imread(self.last_image))

    def create_gif(self):
        """
            Создаёт GIF с пошаговым прохождением пути.
        """
        self.images = []
        self._draw_base_maze()
        path = self.maze_data.solution_coordinates
        for i in range(1, len(path)):
            self._draw_path_frame([path[i-1], path[i]])

        imageio.mimsave(app_settings.gif_file_path, self.images, duration=self.delay)
        

from ..services.generating_maze import GeneratingMaze
from ..services.solution_maze import BFS
import numpy as np


if __name__ == "__main__":
    maze_data = MazeDataWithSolution(
        rows=app_settings.MAZE_ROWS,
        cols=app_settings.MAZE_COLS)
    generating_services = GeneratingMaze(maze_data=maze_data)
    generating_services.create_maze()
    maze_data.start_point = (np.random.randint(0, maze_data.rows), np.random.randint(0, maze_data.cols))
    maze_data.end_point = (np.random.randint(0, maze_data.rows), np.random.randint(0, maze_data.cols))
    # print(f"info (x,y) - start: { \
    #     (maze_data.start_point[1] + 1, maze_data.start_point[0] + 1)} / \
    #     end: {(maze_data.end_point[1] + 1, maze_data.end_point[0] + 1)}")
    solution_services = BFS(maze_data)
    solution_services.finding_way()
    gif = MazeGIF(maze_data)
    gif.create_gif()
