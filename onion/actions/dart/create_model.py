from pathlib import Path
from onion.mediators import Mediator
from onion.templates.dart.model_template import get_model_template
from onion.utils.string_utils import get_entity_name_variations


def create_model(
    input_name: str,
    output_dir: str = ".",
    lib_path: bool = False,
) -> None:
    variations = get_entity_name_variations(input_name)
    single_name = variations.single_name

    if lib_path:
        models_path = Path(output_dir) / "lib" / "src" / "models"
    else:
        models_path = Path(output_dir) / "models"

    if not models_path.exists():
        models_path.mkdir(parents=True)

    model_file = models_path / f"{single_name}_model.dart"
    model_file.write_text(get_model_template(input_name))

    Mediator().output_folders.append(str(models_path))
