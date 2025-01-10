import imageio.v2 as imageio
import matplotlib.pyplot as plt
from settings import app_settings
from models.maze_data_with_solution import MazeDataWithSolution


class MazeGIF:
    def __init__(self, maze_data: MazeDataWithSolution = None, delay: float = 0.3):
        """
            :param maze_data: Объект MazeDataWithSolution с данными лабиринта и путём.
            :param delay: Время задержки между кадрами в секундах.
        """
        self.maze_data = maze_data
        self.delay = delay
        self.images = []
        self.last_image = None
        self._shift = +0.5

    @property
    def maze_data(self) -> MazeDataWithSolution:
        return self.__maze_data

    @maze_data.setter
    def maze_data(self, maze_data) -> None:
        if maze_data is not None:
            self.__maze_data = maze_data
        
    def _x_limit(self):
        """
            Возращает пределы координат изображения по оси x
        """
        return -0.1 * app_settings.WALL_THICKNESS, self.maze_data.cols + 0.1 * app_settings.WALL_THICKNESS

    def _y_limit(self):
        """
            Возращает пределы координат изображения по оси y
        """
        return -0.1 * app_settings.WALL_THICKNESS, self.maze_data.rows + 0.1 * app_settings.WALL_THICKNESS
    
    
    async def _draw_wals(self):
        maze = self.maze_data
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
                if j == 0:
                    plt.plot(
                        [j, j], 
                        [i, i + 1], 
                        color=app_settings.WALL_COLOR, 
                        linewidth=app_settings.WALL_THICKNESS
                    )
                if i == 0:
                    plt.plot(
                        [j, j + 1], 
                        [i, i], 
                        color=app_settings.WALL_COLOR, 
                        linewidth=app_settings.WALL_THICKNESS
                    )

    
    async def _draw_base_maze(self):
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

        await self._draw_wals()
    
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

    async def _draw_path_frame(self, path_segment):
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

    async def create_gif(self, maze_data: MazeDataWithSolution = None):
        """
            Создаёт GIF с пошаговым прохождением пути.
        """
        self.maze_data = maze_data
        self.images = []
        await self._draw_base_maze()
        path = self.maze_data.solution_coordinates
        for i in range(1, len(path)):
            await self._draw_path_frame([path[i-1], path[i]])

        imageio.mimsave(app_settings.gif_file_path, self.images, duration=self.delay)
