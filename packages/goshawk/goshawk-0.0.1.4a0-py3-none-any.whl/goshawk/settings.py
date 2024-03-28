from pathlib import Path

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = "some_secret"
    MODELS_PATH: DirectoryPath = Path("models")
