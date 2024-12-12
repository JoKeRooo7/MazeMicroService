import numpy as np
import matplotlib.pyplot as plt
import imageio
from typing import List, Tuple


class MazeGifGenerator:
    def __init__(self, 
                 rows: int, 
                 cols: int, 
                 right_walls: np.ndarray, 
                 lower_walls: np.ndarray, 
                 start_point: Tuple[int, int], 
                 end_point: Tuple[int, int], 
                 solution_coordinates: List[Tuple[int, int]]):
        self.rows = rows
        self.cols = cols
        self.right_walls = right_walls
        self.lower_walls = lower_walls
        self.start_point = start_point
        self.end_point = end_point
        self.solution_coordinates = solution_coordinates

    def _initialize_figure(self):
        """Создает и возвращает фигуру и ось для отрисовки лабиринта."""
        fig, ax = plt.subplots(figsize=(self.cols, self.rows))
        ax.set_xlim(0, self.cols)
        ax.set_ylim(0, self.rows)
        ax.axis('off')  # Убираем оси
        return fig, ax

    def _draw_maze(self, 
                   ax):
        """Рисует стены лабиринта."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.right_walls[i, j] == 1:
                    ax.plot([j + 1, j + 1], [i, i + 1], color='black')
                if self.lower_walls[i, j] == 1:
                    ax.plot([j, j + 1], [i + 1, i + 1], color='black')

    def _draw_points(self, 
                     ax):
        """Рисует начальную и конечную точки."""
        ax.plot(self.start_point[1] + 0.5, self.start_point[0] + 0.5, 'ro', markersize=14)  # Начало
        ax.plot(self.end_point[1] + 0.5, self.end_point[0] + 0.5, 'ro', markersize=14)  # Конец

    def _draw_path(self, 
                   ax, 
                   step: int):
        """Рисует путь до заданного шага."""
        path = self.solution_coordinates[:step]
        for k in range(len(path) - 1):
            x0, y0 = path[k]
            x1, y1 = path[k + 1]
            ax.plot([y0 + 0.5, y1 + 0.5], [x0 + 0.5, x1 + 0.5], color='red', linewidth=2)

    def generate_gif(self, 
                     gif_path: str, 
                     step_duration: float = 0.6, 
                     wait_duration: float = 30.0) -> float:
        """
        Генерирует GIF-анимацию прохождения лабиринта.
        :param gif_path: Путь для сохранения GIF.
        :param step_duration: Задержка между шагами (в секундах).
        :param wait_duration: Задержка в конце анимации (в секундах).
        :return: Полное время прохождения лабиринта (в секундах).
        """
        frames = []

        # Инициализация фигуры
        fig, ax = self._initialize_figure()
        self._draw_maze(ax)
        self._draw_points(ax)

        # Добавляем начальный кадр
        frames.append(self._fig_to_array(fig))

        # Анимация прохождения пути
        for step in range(1, len(self.solution_coordinates) + 1):
            ax.clear()
            self._draw_maze(ax)
            self._draw_points(ax)
            self._draw_path(ax, step)
            frames.append(self._fig_to_array(fig))

        # Добавляем кадры ожидания в конце
        for _ in range(int(wait_duration / step_duration)):
            frames.append(self._fig_to_array(fig))

        # Сохраняем GIF
        imageio.mimsave(gif_path, frames, duration=step_duration)

        # Возвращаем общее время прохождения лабиринта
        return len(self.solution_coordinates) * step_duration

    @staticmethod
    def _fig_to_array(fig):
        """Преобразует текущую фигуру Matplotlib в массив изображения."""
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        return image

# Пример использования:
# maze = MazeGifGenerator(rows, cols, right_walls, lower_walls, start_point, end_point, solution_coordinates)
# total_time = maze.generate_gif("maze.gif")
# print(f"Total animation time: {total_time} seconds")
