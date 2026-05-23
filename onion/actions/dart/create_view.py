from pathlib import Path
from onion.mediators import Mediator
from onion.templates.dart.view_template import get_view_template
from onion.utils.string_utils import get_entity_name_variations


def create_view(input_name: str, output_dir: str = ".") -> None:
    variations = get_entity_name_variations(input_name)

    plural_name = variations.plural_name

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    view_file = output_path / f"{plural_name}_view.dart"
    view_file.write_text(get_view_template(input_name))

    Mediator().output_folders.append(str(view_file))
