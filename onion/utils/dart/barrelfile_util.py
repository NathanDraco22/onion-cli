from pathlib import Path
from onion.mediators import Mediator


def create_barrel_file(
    directory: str,
    filename: str = "export.dart",
) -> None:
    dir_path = Path(directory)

    if not dir_path.exists():
        raise Exception(f"Directory '{directory}' does not exist")

    dart_files = sorted(
        [
            f.name
            for f in dir_path.iterdir()
            if f.is_file() and f.suffix == ".dart" and f.name != filename
        ]
    )

    exports = "\n".join([f"export '{file}';" for file in dart_files])

    barrel_content = f"""// GENERATED CODE - DO NOT MODIFY BY HAND

{exports}
"""

    barrel_file = dir_path / filename
    barrel_file.write_text(barrel_content)

    Mediator().output_folders.append(str(barrel_file))
