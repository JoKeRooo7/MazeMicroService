from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8888
    GIF_DIRECTORY: str = "files"
    GIF_FILE_NAME: str = "maze.gif"
    MAZE_ROWS: int = 35
    MAZE_COLS: int = 35
    IMAGE_LENGHT: int = 8
    IMAGE_HEIGHT: int = 8
    WALL_COLOR: str = "#000000"
    POINT_COLOR: str = "#28a745"
    WAY_COLOR: str = "#28a745"
    POINT_SIZE: int = 25
    WALL_THICKNESS: int = 3
    GIF_DELAY: float = 0.3


    def __init__(self, **kwargs):
        """
        Переопределяем инициализацию для добавления проверки и создания директории
        """
        super().__init__(**kwargs)
        self.ensure_directory_exists(self.GIF_DIRECTORY)

    @property
    def gif_file_path(self) -> Path:
        """
        Возвращает полный путь к GIF-файлу и создает папку, если её нет
        """
        self.ensure_directory_exists(self.GIF_DIRECTORY)
        return Path(self.GIF_DIRECTORY) / self.GIF_FILE_NAME

    @staticmethod
    def ensure_directory_exists(directory: str):
        """
        Проверяет существование директории и создает её, если необходимо
        """
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


app_settings = Settings()
