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
from onion.templates.dart.view_template import get_view_template
from onion.utils.string_utils import get_entity_name_variations
from onion.utils.dart.relative_path_util import get_relative_prefix
from onion.utils.dart.reactive_repo_util import ensure_reactive_repository, find_package_root


def create_flutter_module(
    input_name: str,
    output_dir: str = ".",
    reactive: bool = False,
) -> None:
    variations = get_entity_name_variations(input_name)
    name = variations.single_name
    plural_name = variations.plural_name

    module_path = Path(output_dir) / plural_name

    cubit_path = module_path / "cubit"
    dialogs_path = module_path / "dialogs"
    view_path = module_path / "view"
    widgets_path = module_path / "widgets"

    cubit_path.mkdir(parents=True, exist_ok=True)
    dialogs_path.mkdir(parents=True, exist_ok=True)
    view_path.mkdir(parents=True, exist_ok=True)
    widgets_path.mkdir(parents=True, exist_ok=True)

    import_prefix = get_relative_prefix(cubit_path, find_package_root(output_dir))

    read_cubit_file = cubit_path / f"read_{plural_name}_cubit.dart"
    read_cubit_file.write_text(
        get_read_cubit_template(name, reactive, import_prefix)
    )

    read_state_file = cubit_path / f"read_{plural_name}_state.dart"
    read_state_file.write_text(get_read_state_template(name))

    write_cubit_file = cubit_path / f"write_{plural_name}_cubit.dart"
    write_cubit_file.write_text(
        get_write_cubit_template(name, reactive, import_prefix)
    )

    write_state_file = cubit_path / f"write_{plural_name}_state.dart"
    write_state_file.write_text(get_write_state_template(name))

    dialogs_init_file = dialogs_path / f"{plural_name}_dialogs.dart"
    dialogs_init_file.write_text(f"// {name} dialogs\n")

    view_init_file = view_path / f"{plural_name}_view.dart"
    view_init_file.write_text(get_view_template(name))

    widgets_init_file = widgets_path / f"{plural_name}_widgets.dart"
    widgets_init_file.write_text(f"// {name} widgets\n")

    if reactive:
        ensure_reactive_repository(output_dir)

    Mediator().output_folders.append(str(module_path))
