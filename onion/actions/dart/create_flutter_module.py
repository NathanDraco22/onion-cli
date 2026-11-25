from pathlib import Path

from onion.actions.dart.create_cubit import create_cubit
from onion.actions.dart.create_view import create_view
from onion.mediators import Mediator
from onion.utils.dart.pubspec_util import require_pubspec_name
from onion.utils.dart.reactive_repo_util import find_package_root
from onion.utils.string_utils import get_entity_name_variations


def create_flutter_module(
    input_name: str,
    output_dir: str = ".",
    reactive: bool = False,
    responsive: bool = False,
    business_package: str | None = None,
) -> None:
    variations = get_entity_name_variations(input_name)
    name = variations.single_name
    plural_name = variations.plural_name

    package_root = find_package_root(output_dir)
    require_pubspec_name(package_root)

    module_path = Path(output_dir) / plural_name
    dialogs_path = module_path / "dialogs"
    view_path = module_path / "view"
    widgets_path = module_path / "widgets"

    dialogs_path.mkdir(parents=True, exist_ok=True)
    view_path.mkdir(parents=True, exist_ok=True)
    widgets_path.mkdir(parents=True, exist_ok=True)

    # Non-global cubits live outside the module: lib/src/cubits/{plural}/.
    cubits_dir = package_root / "lib" / "src" / "cubits"
    create_cubit(
        input_name,
        str(cubits_dir),
        reactive=reactive,
        business_package=business_package,
    )

    # The screen is the only place that instantiates the feature cubits.
    create_view(
        input_name,
        str(view_path),
        responsive=responsive,
        providers=True,
        business_package=business_package,
    )

    dialogs_init_file = dialogs_path / f"{plural_name}_dialogs.dart"
    dialogs_init_file.write_text(f"// {name} dialogs\n", encoding="utf-8")

    widgets_init_file = widgets_path / f"{plural_name}_widgets.dart"
    widgets_init_file.write_text(f"// {name} widgets\n", encoding="utf-8")

    Mediator().output_folders.append(str(module_path))
