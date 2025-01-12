import asyncio
import io
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from settings import app_settings
from models.maze_data_with_solution import MazeDataWithSolution
from asyncio import Semaphore


class MazeGIF:
    def __init__(self, maze_data: MazeDataWithSolution = None, delay: float = 0.3, max_concurrent_tasks: int = 5):
        """
        :param maze_data: Объект MazeDataWithSolution с данными лабиринта и путём.
        :param delay: Время задержки между кадрами в секундах.
        :param max_concurrent_tasks: Максимальное количество одновременных задач для генерации кадров.
        """
        self.maze_data = maze_data
        self.delay = delay
        self._shift = +0.5
        self._semaphore = Semaphore(max_concurrent_tasks)  # Лимитируем количество параллельных задач

    async def _draw_walls(self):
        maze = self.maze_data
        for i in range(maze.rows):
            for j in range(maze.cols):
                if maze.right_walls[i, j]:
                    plt.plot([j + 1, j + 1], [i, i + 1], color=app_settings.WALL_COLOR, linewidth=app_settings.WALL_THICKNESS)
                if maze.lower_walls[i, j]:
                    plt.plot([j, j + 1], [i + 1, i + 1], color=app_settings.WALL_COLOR, linewidth=app_settings.WALL_THICKNESS)
                if j == 0:
                    plt.plot([j, j], [i, i + 1], color=app_settings.WALL_COLOR, linewidth=app_settings.WALL_THICKNESS)
                if i == 0:
                    plt.plot([j, j + 1], [i, i], color=app_settings.WALL_COLOR, linewidth=app_settings.WALL_THICKNESS)

    async def _draw_base_maze(self):
        """
        Отрисовывает лабиринт без решения (только стены, старт и конец), используя буфер.
        """
        maze = self.maze_data
        plt.figure(figsize=(app_settings.IMAGE_LENGHT, app_settings.IMAGE_HEIGHT))
        await self._draw_walls()

        plt.scatter(
            maze.start_point[1] + self._shift,
            maze.start_point[0] + self._shift,
            color=app_settings.POINT_COLOR,
            s=app_settings.POINT_SIZE,
            marker="v",
            label="Start"
        )
        plt.scatter(
            maze.end_point[1] + self._shift,
            maze.end_point[0] + self._shift,
            color=app_settings.POINT_COLOR,
            s=app_settings.POINT_SIZE,
            marker="s",
            label="End"
        )

        plt.xlim(-0.1 * app_settings.WALL_THICKNESS, maze.cols + 0.1 * app_settings.WALL_THICKNESS)
        plt.ylim(-0.1 * app_settings.WALL_THICKNESS, maze.rows + 0.1 * app_settings.WALL_THICKNESS)
        plt.axis("off")
        plt.gca().invert_yaxis()
        plt.tight_layout(pad=0)

        # Используем asyncio.to_thread для асинхронного сохранения изображения
        buf = await asyncio.to_thread(self._save_base_maze)
        return buf

    def _save_base_maze(self):
        """Сохранение изображения в буфер, это синхронный метод для использования в потоках."""
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
        buf.seek(0)
        plt.close()
        return buf

    async def _yield_path_frames(self):
        """
        Генератор для создания кадров пути пошагово с использованием памяти, а не файлов.
        """
        base_image_buf = await self._draw_base_maze()
        base_image = await asyncio.to_thread(plt.imread, base_image_buf)

        path = self.maze_data.solution_coordinates
        for i in range(1, len(path)):
            y1, x1 = path[i - 1]
            y2, x2 = path[i]

            async with self._semaphore:  # Ожидаем освобождения ресурса
                plt.figure(figsize=(app_settings.IMAGE_LENGHT, app_settings.IMAGE_HEIGHT))
                plt.imshow(base_image, extent=[
                    -0.1 * app_settings.WALL_THICKNESS,
                    self.maze_data.cols + 0.1 * app_settings.WALL_THICKNESS,
                    -0.1 * app_settings.WALL_THICKNESS,
                    self.maze_data.rows + 0.1 * app_settings.WALL_THICKNESS
                ])
                plt.plot(
                    [x2 + self._shift, x1 + self._shift],
                    [self.maze_data.rows - y2 - self._shift, self.maze_data.rows - y1 - self._shift],
                    color=app_settings.WAY_COLOR
                )
                plt.axis("off")
                plt.tight_layout(pad=0)

                # Сохраняем кадр в буфер, чтобы передать его в gif
                buf = await asyncio.to_thread(self._save_frame)
                yield buf
                buf.close()

    def _save_frame(self):
        """Сохранение кадра в буфер, метод для использования в потоке."""
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
        buf.seek(0)
        plt.close()
        return buf


    async def create_gif(self, maze_data: MazeDataWithSolution = None):
        """
        Создаёт GIF с пошаговым прохождением пути.
        """
        self.maze_data = maze_data
        frame_generator = self._yield_path_frames()

        with imageio.get_writer(app_settings.gif_file_path, mode='I', duration=self.delay) as writer:
            async for frame_buf in frame_generator:
                frame = await asyncio.to_thread(imageio.imread, frame_buf)
                writer.append_data(frame)
                frame_buf.close()
