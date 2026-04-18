from typer import Typer
from typer import Argument, Option
from rich import print
from onion.mediators import Mediator
from onion.actions.create_repo import create_repo
from onion.actions.create_repo_with_mongo_collection import (
    create_repo_with_mongo_collection,
)
from onion.actions.create_router import create_router
from onion.actions.create_router_with_module import create_router_with_module
from onion.actions.create_router_with_repo_with_mongo import (
    create_router_with_repo_with_mongo,
)
from onion.actions.dart.create_datasource import create_datasource
from onion.actions.dart.create_repository import create_repository
from onion.actions.dart.create_cubit import create_cubit
from onion.actions.dart.create_flutter_module import create_flutter_module
from onion.actions.dart.create_model import create_model
from onion.actions.project.copy_flutter_project import copy_flutter_project
from onion.actions.project.copy_fastapi_project import copy_fastapi_project
from onion.actions.project.copy_fastapi_full_project import copy_fastapi_full_project

from onion.utils.string_utils import is_plural_english
from onion.utils.dart.barrelfile_util import create_barrel_file

app = Typer()

project_app = Typer(
    help="overwrite lib folder with Flutter template, app folder with FastAPI template"
)
app.add_typer(project_app, name="project")


@project_app.command(help="create lib folder from Flutter template")
def flutter_lib(
    output_dir: str = Argument(
        default=".", help="project directory (default: current directory)"
    ),
    package: str = Option(
        default="com.example.app",
        help="package name (default: com.example.app)",
    ),
    force: bool = Option(
        default=False,
        help="force overwrite if lib folder exists",
    ),
):
    copy_flutter_project(output_dir, package, force)

    print("[green]flutter lib folder created :heavy_check_mark:[/green]")
    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


@project_app.command(help="create app folder from FastAPI template")
def fastapi_app(
    output_dir: str = Argument(
        default=".",
        help="project directory (default: current directory)",
    ),
    force: bool = Option(
        default=False,
        help="force overwrite if app folder exists",
    ),
):
    copy_fastapi_project(output_dir, force)

    print("[green]fastapi project created :heavy_check_mark:[/green]")
    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


@project_app.command(help="initialize complete FastAPI project from template")
def fastapi_init(
    output_dir: str = Argument(
        help="project directory",
    ),
    force: bool = Option(
        default=False,
        help="force overwrite if directory exists",
    ),
):
    copy_fastapi_full_project(output_dir, force)

    print("[green]fastapi project initialized :heavy_check_mark:[/green]")
    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


@app.command(help="create router, controller and module")
def crud(
    names: list[str] = Argument(help="module name or list of names"),
    version: int = Option(help="version example: 1"),
):
    for name in names:
        if is_plural_english(name):
            raise Exception("plural names are not allowed")

    for name in names:
        create_router_with_module(name, version)

    print("[green]router and module created :heavy_check_mark:[/green]")
    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


@app.command(help="create router, controller, module, mongo collection")
def crud_mongo(
    names: list[str] = Argument(help="module name or list of names"),
    version: int = Option(help="version example: 1"),
):
    for name in names:
        if is_plural_english(name):
            raise Exception("plural names are not allowed")

    for name in names:
        create_router_with_repo_with_mongo(name, version)

    print(
        "[green]router, repository and mongo collection created :heavy_check_mark:[/green]"
    )
    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


@app.command(help="create a module")
def repo(
    names: list[str] = Argument(help="module name"),
    version: int = Option(help="version example: 1"),
):
    for name in names:
        if is_plural_english(name):
            raise Exception("plural names are not allowed")

    for name in names:
        create_repo(name, version)

    print("[green]repository created :heavy_check_mark:[/green]")
    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


@app.command(help="create a module with mongo collection")
def repo_mongo(
    names: list[str] = Argument(help="module name"),
    version: int = Option(help="version example: 1"),
):
    for name in names:
        if is_plural_english(name):
            raise Exception("plural names are not allowed")

    for name in names:
        create_repo_with_mongo_collection(name, version)

    print("[green]repository with mongo collection created :heavy_check_mark:[/green]")
    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


@app.command(help="create a router")
def router(
    names: list[str] = Argument(help="router name"),
    version: int = Option(help="version example: 1"),
):
    for name in names:
        if is_plural_english(name):
            raise Exception("plural names are not allowed")

    for name in names:
        create_router(name, version)

    print("[green]router created :heavy_check_mark:[/green]")

    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


@app.command(help="create datasource, repository and models for Dart/Flutter")
def dart(
    name: str = Argument(help="entity name (e.g., unit, product, client)"),
    output_dir: str = Option(
        default="./lib/src",
        help="project directory (default: current directory)",
    ),
):
    if is_plural_english(name):
        raise Exception("plural names are not allowed")

    create_model(name, output_dir, lib_path=True)
    create_datasource(name, output_dir)
    create_repository(name, output_dir)

    print(
        "[green]dart datasource, repository and models created :heavy_check_mark:[/green]"
    )

    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


@app.command(help="create models for Dart/Flutter (Base, Create, Update, InDb)")
def dart_model(
    name: str = Argument(help="entity name (e.g., unit, product, client)"),
    output_dir: str = Option(
        default=".",
        help="project directory (default: current directory)",
    ),
):
    if is_plural_english(name):
        raise Exception("plural names are not allowed")

    create_model(name, output_dir)

    print("[green]dart model created :heavy_check_mark:[/green]")

    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


@app.command(help="create cubits for Dart/Flutter")
def dart_cubit(
    name: str = Argument(help="entity name (e.g., unit, product, client)"),
    output_dir: str = Option(
        default=".",
        help="project directory (default: current directory)",
    ),
    read_only: bool = Option(
        default=False,
        help="only create read cubit",
    ),
    write_only: bool = Option(
        default=False,
        help="only create write cubit",
    ),
):
    if is_plural_english(name):
        raise Exception("plural names are not allowed")

    create_cubit(name, output_dir, read_only, write_only)

    print("[green]dart cubit(s) created :heavy_check_mark:[/green]")

    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


@app.command(help="create Flutter module with cubit, dialogs, view, widgets")
def flutter_module(
    name: str = Argument(help="entity name (e.g., unit, product, client)"),
    output_dir: str = Option(
        default=".",
        help="project directory (default: current directory)",
    ),
):
    if is_plural_english(name):
        raise Exception("plural names are not allowed")

    create_flutter_module(name, output_dir)

    print("[green]flutter module created :heavy_check_mark:[/green]")

    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")


if __name__ == "__main__":
    app()


@app.command(help="create barrel file (export.dart) in a directory")
def barrel(
    directory: str = Argument(help="directory to create barrel file"),
    filename: str = Option(
        default="export.dart",
        help="barrel filename (default: export.dart)",
    ),
):
    create_barrel_file(directory, filename)

    print("[green]barrel file created :heavy_check_mark:[/green]")

    for folder in Mediator().output_folders:
        print(f"[yellow]{folder}[/yellow]")
