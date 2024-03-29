import os
from pathlib import Path
from pydantic_settings import BaseSettings

current_working_directory = Path.cwd()

# print output to the console
print(f'current_working_directory={current_working_directory}')
filepath=os.path.join(os.path.dirname(__file__), '..','models')
print(filepath)


class Settings(BaseSettings):
    API_KEY: str = "some_secret"
    MODELS_PATH: str = filepath #os.path.abspath("models")

