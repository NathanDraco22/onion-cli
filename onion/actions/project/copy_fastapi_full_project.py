import os
import shutil
import stat
import subprocess
from pathlib import Path

from onion.utils.string_utils import get_entity_name_variations
from onion.mediators import Mediator

TEMPLATE_REPO_URL = "https://github.com/NathanDraco22/fastapi-onion-template.git"


def _remove_readonly(func, path, exc_info) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def force_remove_tree(path: Path) -> None:
    shutil.rmtree(path, onexc=_remove_readonly)


def copy_fastapi_full_project(
    output_dir: str,
    force: bool = False,
) -> None:
    output_path = Path(output_dir)

    if output_path.exists() and not force:
        raise Exception(
            f"Directory '{output_dir}' already exists. Use --force to overwrite"
        )

    if output_path.exists():
        force_remove_tree(output_path)

    try:
        subprocess.run(
            ["git", "clone", TEMPLATE_REPO_URL, str(output_path)],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as error:
        raise Exception(
            f"Failed to clone template '{TEMPLATE_REPO_URL}': "
            f"{error.stderr.decode(errors='replace').strip()}"
        )

    git_dir = output_path / ".git"
    if git_dir.exists():
        force_remove_tree(git_dir)

    project_name = output_path.name
    if not project_name or project_name == ".":
        project_name = "app"

    variations = get_entity_name_variations(project_name)
    entity_name = variations.single_name
    entity_name_plural = variations.plural_name
    EntityName = variations.Name
    EntityNamePlural = variations.Name_plural

    replace_in_directory(output_path, "examples", entity_name_plural)
    replace_in_directory(output_path, "Examples", EntityNamePlural)
    replace_in_directory(output_path, "example", entity_name)
    replace_in_directory(output_path, "Example", EntityName)

    rename_directories(output_path, "examples", entity_name_plural)
    rename_directories(output_path, "Examples", EntityNamePlural)

    for ext in [".py"]:
        rename_files_in_directory(output_path, "examples", entity_name_plural)
        rename_files_in_directory(output_path, "Examples", EntityNamePlural)
        rename_files_in_directory(output_path, "example", entity_name)
        rename_files_in_directory(output_path, "Example", EntityName)

    rename_project_in_pyproject(output_path, project_name)

    Mediator().output_folders.append(output_dir)


def rename_project_in_pyproject(output_path: Path, project_name: str) -> None:
    pyproject_path = output_path / "pyproject.toml"
    if not pyproject_path.exists():
        return

    content = pyproject_path.read_text(encoding="utf-8")
    content = content.replace(
        'name = "fastapi-onion-template"',
        f'name = "{project_name}"',
    )
    content = content.replace(
        'description = "Add your description here"',
        f'description = "{project_name} API"',
    )
    pyproject_path.write_text(content, encoding="utf-8")


def replace_in_directory(directory: Path, old: str, new: str) -> None:
    for file_path in directory.rglob("*"):
        if file_path.is_file() and file_path.suffix in [
            ".py",
            ".md",
            ".yaml",
            ".json",
            ".toml",
            ".txt",
        ]:
            try:
                content = file_path.read_text(encoding="utf-8")
                if old in content:
                    content = content.replace(old, new)
                    file_path.write_text(content, encoding="utf-8")
            except Exception:
                pass


def rename_files_in_directory(directory: Path, old: str, new: str) -> None:
    for file_path in list(directory.rglob(f"*{old}*")):
        if old in file_path.name and file_path.is_file():
            new_name = file_path.name.replace(old, new)
            new_path = file_path.parent / new_name
            if not new_path.exists():
                file_path.rename(new_path)


def rename_directories(directory: Path, old: str, new: str) -> None:
    for dir_path in list(directory.rglob(old)):
        if dir_path.is_dir():
            new_dir_path = dir_path.parent / new
            if not new_dir_path.exists():
                dir_path.rename(new_dir_path)
