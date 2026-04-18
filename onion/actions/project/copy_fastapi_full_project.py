import shutil
from pathlib import Path
from onion.utils.string_utils import get_entity_name_variations
from onion.mediators import Mediator


def copy_fastapi_full_project(
    output_dir: str,
    force: bool = False,
) -> None:
    base_path = Path("onion/project_base/fast_api_app")
    output_path = Path(output_dir)

    if output_path.exists() and not force:
        raise Exception(
            f"Directory '{output_dir}' already exists. Use --force to overwrite"
        )

    if output_path.exists():
        shutil.rmtree(output_path)

    shutil.copytree(base_path, output_path)

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

    Mediator().output_folders.append(output_dir)


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
