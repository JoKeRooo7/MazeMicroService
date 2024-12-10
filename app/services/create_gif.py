import numpy as np
import matplotlib.pyplot as plt
import imageio
from typing import List, Tuple



# def generate_maze_gif(maze: MazeDataWithSolution, gif_path: str):
#     frames = []
#     rows, cols = maze.rows, maze.cols

#     fig, ax = plt.subplots(figsize=(cols, rows))
#     ax.plot([0, cols], [0, 0], color='black')
#     ax.plot([0, cols], [rows, rows], color='black')
#     ax.plot([0, 0], [0, rows], color='black')
#     ax.plot([cols, cols], [0, rows], color='black')

#     # Рисуем стены лабиринта
#     for i in range(rows):
#         for j in range(cols):
#             # Рисуем правую стену
#             if maze.right_walls[i, j] == 1:
#                 ax.plot([j + 1, j + 1], [i, i + 1], color='black')
#             # Рисуем нижнюю стену
#             if maze.lower_walls[i, j] == 1:
#                 ax.plot([j, j + 1], [i + 1, i + 1], color='black')

    
#     ax.plot(maze.start_point[1] + 0.5, maze.start_point[0] + 0.5, 'go', markersize=10)
#     ax.plot(maze.end_point[1] + 0.5, maze.end_point[0] + 0.5, 'ro', markersize=10)


#     path = maze.solution_coordinates
#     if path:
#         for k in range(len(path) - 1):
#             x0, y0 = path[k]
#             x1, y1 = path[k + 1]
#             ax.plot([y0 + 0.5, y1 + 0.5], [x0 + 0.5, x1 + 0.5], color='red', linewidth=2)

#     # Сохраняем кадры в список
#     frames.append(fig_to_array(fig))

#     # Процесс анимации: рисуем шаги по пути
#     for step in range(1, len(path) + 1):
#         # Очистить и перерисовать лабиринт на каждом шаге
#         ax.clear()
#         ax.plot([0, cols], [0, 0], color='black')  # Верхняя граница
#         ax.plot([0, cols], [rows, rows], color='black')  # Нижняя граница
#         ax.plot([0, 0], [0, rows], color='black')  # Левая граница
#         ax.plot([cols, cols], [0, rows], color='black')  # Правая граница

#         # Рисуем стены
#         for i in range(rows):
#             for j in range(cols):
#                 if maze.right_walls[i, j] == 1:
#                     ax.plot([j + 1, j + 1], [i, i + 1], color='black')
#                 if maze.lower_walls[i, j] == 1:
#                     ax.plot([j, j + 1], [i + 1, i + 1], color='black')

#         # Рисуем начальную и конечную точки
#         ax.plot(maze.start_point[1] + 0.5, maze.start_point[0] + 0.5, 'go', markersize=10)  # Начало
#         ax.plot(maze.end_point[1] + 0.5, maze.end_point[0] + 0.5, 'ro', markersize=10)  # Конец

#         # Рисуем путь до текущего шага
#         path_until_step = path[:step]
#         for k in range(len(path_until_step) - 1):
#             x0, y0 = path_until_step[k]
#             x1, y1 = path_until_step[k + 1]
#             ax.plot([y0 + 0.5, y1 + 0.5], [x0 + 0.5, x1 + 0.5], color='red', linewidth=2)

#         # Добавляем кадр
#         frames.append(fig_to_array(fig))

#     # Добавляем 30 секунд ожидания в начало (30 секунд * 10 кадров в секунду = 300 кадров)
#     for _ in range(300):
#         frames.append(fig_to_array(fig))

#     # Сохраняем GIF
#     imageio.mimsave(gif_path, frames, dura)

