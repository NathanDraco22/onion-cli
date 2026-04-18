from pathlib import Path
from onion.mediators import Mediator
from onion.templates.dart.read_cubit_template import (
    get_read_cubit_template,
    get_read_state_template,
)
from onion.templates.dart.write_cubit_template import (
    get_write_cubit_template,
    get_write_state_template,
)
from onion.utils.string_utils import get_entity_name_variations


def create_cubit(
    input_name: str,
    output_dir: str = ".",
    only_read: bool = False,
    only_write: bool = False,
) -> None:
    variations = get_entity_name_variations(input_name)
    name = variations.single_name
    plural_name = variations.plural_name

    dest_dir = Path(output_dir / Path(f"{name}_cubit"))

    cubit_path = Path(dest_dir)
    if not cubit_path.exists():
        cubit_path.mkdir(parents=True)

    if not only_write:
        read_cubit_file = cubit_path / f"read_{plural_name}_cubit.dart"
        read_cubit_file.write_text(get_read_cubit_template(name))

        read_state_file = cubit_path / f"read_{plural_name}_state.dart"
        read_state_file.write_text(get_read_state_template(name))

    if not only_read:
        write_cubit_file = cubit_path / f"write_{plural_name}_cubit.dart"
        write_cubit_file.write_text(get_write_cubit_template(name))

        write_state_file = cubit_path / f"write_{plural_name}_state.dart"
        write_state_file.write_text(get_write_state_template(name))

    Mediator().output_folders.append(str(cubit_path))
