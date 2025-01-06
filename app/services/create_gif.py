import numpy as np
import matplotlib.pyplot as plt
import imageio
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
        self.base_image_path = "/tmp/maze_base.png"

    def _draw_base_maze(self):
        """ Отрисовывает лабиринт без решения (только стены, старт и конец). """
        maze = self.maze_data
        plt.figure(figsize=(8, 8))

        for i in range(maze.rows):
            for j in range(maze.cols):
                if maze.right_walls[i, j]:
                    plt.plot([j + 1, j + 1], [i, i + 1], color="black")
                if maze.lower_walls[i, j]:
                    plt.plot([j, j + 1], [i + 1, i + 1], color="black")

        # Отрисовка точки старта и конца
        plt.scatter(maze.start_point[1], maze.start_point[0], color="green", s=100, label="Start")
        plt.scatter(maze.end_point[1], maze.end_point[0], color="red", s=100, label="End")

        # Настройка осей
        plt.xlim(-1, maze.cols + 1)
        plt.ylim(-1, maze.rows + 1)
        plt.axis("off")
        plt.gca().invert_yaxis()  # переворот по вертикали
        # plt.legend()
        plt.tight_layout()

        # Сохранение базового изображения
        plt.savefig(self.base_image_path)
        plt.close()

    def _draw_path_frame(self):
        """ Добавляет текущий путь на базовый фон и сохраняет кадр. """
        base_image = plt.imread(self.base_image_path)
        plt.figure(figsize=(8, 8))
        plt.imshow(base_image, extent=[-1, self.maze_data.cols + 1, -1, self.maze_data.rows + 1])
        current_path = self.maze_data.solution_coordinates
        # Рисование текущего пути
        for (x1, y1), (x2, y2) in zip(current_path, current_path[1:]):
            plt.plot([y1, y2], [x1, x2], color="blue")

        plt.axis("off")
        plt.gca().invert_yaxis()
        plt.tight_layout()

        # Сохранение кадра
        frame_path = f"/tmp/frame_{len(self.images)}.png"
        plt.savefig(frame_path)
        plt.close()
        self.images.append(imageio.imread(frame_path))

    def create_gif(self, filename: str):
        """Создаёт GIF с пошаговым прохождением пути. """
        self._draw_base_maze()  # Рисуем фон лабиринта один раз
        path = self.maze_data.solution_coordinates
        current_path = []

        for step in range(len(path)):
            current_path.append(path[step])
            self.draw_path_frame(current_path)

        # Сохранение итогового GIF с задержкой
        imageio.mimsave(filename, self.images, duration=self.delay)
        print(f"GIF сохранён как {filename}")

# Пример использования
if __name__ == "__main__":
    # Пример данных лабиринта
    maze_data = MazeDataWithSolution(
        rows=5,
        cols=5,
        right_walls=np.random.choice([0, 1], size=(5, 5)),
        lower_walls=np.random.choice([0, 1], size=(5, 5)),
        start_point=(0, 0),
        end_point=(4, 4),
        solution_coordinates=[
            (0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4)
        ]
    )

    gif_creator = MazeGIF(maze_data, delay=0.5)
    gif_creator.create_gif("maze_solution.gif")