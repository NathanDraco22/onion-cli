from pathlib import Path
from onion.mediators import Mediator
from onion.templates.dart.repository_template import get_repository_template
from onion.utils.string_utils import get_entity_name_variations
from onion.utils.dart.barrelfile_util import create_barrel_file
from onion.utils.dart.reactive_repo_util import ensure_reactive_repository


def create_repository(
    input_name: str,
    output_dir: str = ".",
    reactive: bool = False,
) -> None:
    variations = get_entity_name_variations(input_name)
    name = variations.single_name
    filename = f"{variations.plural_name}_repository.dart"

    output_path = Path(output_dir) / "domain" / "repositories"
    if not output_path.exists():
        output_path.mkdir(parents=True)

    repository_file_path = output_path / filename
    repository_file_path.write_text(get_repository_template(name, reactive))

    create_barrel_file(str(output_path), "repositories.dart")

    if reactive:
        ensure_reactive_repository(output_dir)

    Mediator().output_folders.append(f"{output_path / filename}")
    Mediator().output_folders.append(f"{output_path / 'repositories.dart'}")
