import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = "some_secret"
    MODELS_PATH: str = os.path.abspath("models")
