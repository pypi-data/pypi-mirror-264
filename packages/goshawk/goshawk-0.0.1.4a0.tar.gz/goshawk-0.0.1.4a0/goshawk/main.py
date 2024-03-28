import importlib.metadata
from typing import List, Optional

import typer
from typing_extensions import Annotated

from .settings import Settings
from goshawk.visuals.view_model_tree import view_model_tree as vmt

app_settings = Settings()
app = typer.Typer(no_args_is_help=True)



@app.callback(invoke_without_command=True)
def main(version: bool = False) -> None:
    """
    Output the version #
    """
    if version:
        print(importlib.metadata.metadata("goshawk")["Version"])



@app.command()
def view_model_tree(
    mask: Annotated[
        Optional[List[str]],
        typer.Option(help="Mask to deploy"),
    ] = None,
    schemas_only: Annotated[bool, typer.Option("--schemas-only")] = False,
) -> None:
    print("View model tre")
    if schemas_only:
        vmt()


@app.command()
def data_refresh(
    db_env: Annotated[str, typer.Option(help="Name of db environment")] = "",
    mask: Annotated[Optional[List[str]], typer.Option(help="Mask to deploy")] = None,
    #    version: Annotated[Optional[bool], typer.Option("--version", callback=version_callback)] = None,
) -> None:
    print("Data refresh")


@app.command()
def model_deploy(
    db_env: Annotated[str, typer.Option(help="Name of db environment")] = "",
    mask: Annotated[Optional[List[str]], typer.Option(help="Mask to deploy")] = None,
) -> None:
    print(f"Model deploy dbenv={db_env},mask={mask} ")


@app.command()
def init_env(envname: str) -> None:
    print(f"Creating environment: {envname}")


@app.command()
def destroy_env(envname: str) -> None:
    print(f"Destroying environment: {envname}")


if __name__ == "__main__":
    app()
