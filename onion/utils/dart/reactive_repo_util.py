from pathlib import Path

from onion.mediators import Mediator
from onion.templates.dart.reactive_repository_template import (
    get_reactive_repository_template,
)


def find_package_root(output_dir: str) -> Path:
    current = Path(output_dir).resolve()
    for folder in [current, *current.parents]:
        if (folder / "pubspec.yaml").exists():
            return folder
    return Path(output_dir)


def ensure_reactive_repository(output_dir: str) -> str:
    package_root = find_package_root(output_dir)
    file_path = (
        package_root / "lib" / "src" / "tools" / "reactive_repo" / "reactive_repository.dart"
    )
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(get_reactive_repository_template())
        Mediator().output_folders.append(str(file_path))
    return str(file_path)
