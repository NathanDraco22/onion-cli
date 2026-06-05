from pathlib import Path
from onion.mediators import Mediator
from onion.templates.dart.response_template import get_list_response_template


def create_list_response(output_dir: str = ".") -> None:
    output_path = Path(output_dir)
    if not output_path.exists():
        output_path.mkdir(parents=True)

    response_file = output_path / "list_response.dart"
    response_file.write_text(get_list_response_template())

    Mediator().output_folders.append(str(response_file))
