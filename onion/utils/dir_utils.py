from pathlib import Path
from onion.mediators import Mediator


def _get_base_path(fallback: str) -> Path:
    user_folder = Mediator().user_output_folder
    return Path(user_folder) if user_folder else Path(fallback)


def create_repos_directory(name: str, version: int) -> Path:
    base_folder = _get_base_path("app")
    if not base_folder.exists():
        base_folder.mkdir()

    # check "repos" folder
    module_folder_path = base_folder / "repos"
    if not module_folder_path.exists():
        module_folder_path.mkdir()

    # check "repos/v{version}" folder
    version_folder_path = module_folder_path / f"v{version}"
    if not version_folder_path.exists():
        version_folder_path.mkdir()

    # check "repos/v{version}/{name}" folder
    output_folder_path = version_folder_path / name
    if not output_folder_path.exists():
        output_folder_path.mkdir()

    return output_folder_path


def create_generated_output_directory(name: str) -> Path:
    base_folder = _get_base_path("generated_output")
    if not base_folder.exists():
        base_folder.mkdir()

    # check "generated/{name}" folder
    output_folder_path = base_folder / name
    if not output_folder_path.exists():
        output_folder_path.mkdir()

    return output_folder_path
