import shutil
from pathlib import Path
from onion.utils.string_utils import get_entity_name_variations
from onion.mediators import Mediator


def copy_flutter_project(
    output_dir: str,
    package_name: str = "com.example.app",
    force: bool = False,
) -> None:
    base_path = Path("onion/project_base/flutter_app")
    output_path = Path(output_dir)
    lib_path = output_path / "lib"

    if lib_path.exists() and not force:
        raise Exception(
            f"Directory '{output_dir}/lib' already exists. Use --force to overwrite"
        )

    lib_base_path = base_path / "lib"

    if lib_path.exists():
        shutil.rmtree(lib_path)
    shutil.copytree(lib_base_path, lib_path)

    project_name = output_path.name
    variations = get_entity_name_variations(project_name)
    entity_name = variations.single_name
    EntityName = variations.Name

    replace_in_directory(lib_path, "sample", entity_name)
    replace_in_directory(lib_path, "Sample", EntityName)
    replace_in_directory(lib_path, "sample_entity", entity_name)
    replace_in_directory(lib_path, "SampleEntity", EntityName)
    replace_in_directory(lib_path, "kardex_app_front", package_name.replace(".", "_"))

    for ext in [".dart", ".yaml", ".json"]:
        rename_files_in_directory(lib_path, "sample", entity_name)
        rename_files_in_directory(lib_path, "Sample", EntityName)

    Mediator().output_folders.append(f"{output_dir}/lib")


def replace_in_directory(directory: Path, old: str, new: str) -> None:
    for file_path in directory.rglob("*"):
        if file_path.is_file() and file_path.suffix in [
            ".dart",
            ".yaml",
            ".json",
            ".md",
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
