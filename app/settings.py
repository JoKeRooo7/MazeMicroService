from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_HOST: str = Field("0.0.0.0", env="HOST")
    APP_PORT: int = Field(8888, env="PORT")
    GIF_DIRECTORY: str = Field("files", env="MAZE_GIF_DIRECTORY")
    GIF_FILE_NAME: str = Field("maze.gif", env="MAZE_GIF_FILE_NAME")
    MAZE_ROWS: int = Field(35, env="MAZE_STD_ROWS")
    MAZE_COLS: int = Field(35, env="MAZE_STD_COLS")
    IMAGE_LENGHT: int = Field(8, env="MAZE_IMAGE_LENGHT")
    IMAGE_HEIGHT: int = Field(8, env="MAZE_IMAGE_HEIGHT")
    WALL_COLOR: str = Field("#000000", env="MAZE_WALL_COLOR")
    POINT_COLOR: str = Field("#28a745", env="MAZE_POINT_COLOR")
    WAY_COLOR: str = Field("#28a745", env="MAZE_WAY_COLOR")
    POINT_SIZE: int = Field(25, env="MAZE_POINT_SIZE")
    WALL_THICKNESS: int = Field(3, env="MAZE_WALL_THICKNESS")
    GIF_DELAY: float = Field(0.3, env="MAZE_WALL_THICKNESS")


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
