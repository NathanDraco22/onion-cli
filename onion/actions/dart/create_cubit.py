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
from onion.utils.dart.relative_path_util import get_relative_prefix
from onion.utils.dart.reactive_repo_util import ensure_reactive_repository, find_package_root


def create_cubit(
    input_name: str,
    output_dir: str = ".",
    only_read: bool = False,
    only_write: bool = False,
    reactive: bool = False,
    business_package: str | None = None,
) -> None:
    variations = get_entity_name_variations(input_name)
    name = variations.single_name
    plural_name = variations.plural_name

    cubit_path = Path(output_dir) / plural_name
    if not cubit_path.exists():
        cubit_path.mkdir(parents=True)

    import_prefix = ""
    if not business_package:
        try:
            import_prefix = get_relative_prefix(
                cubit_path, find_package_root(output_dir)
            )
        except ValueError as exc:
            raise ValueError(
                "Cubits outside lib/src require --business-package so their "
                "imports use the business package barrel."
            ) from exc

    if not only_write:
        read_cubit_file = cubit_path / f"read_{plural_name}_cubit.dart"
        read_cubit_file.write_text(
            get_read_cubit_template(
                name,
                reactive,
                import_prefix,
                business_package,
            ),
            encoding="utf-8",
        )

        read_state_file = cubit_path / f"read_{plural_name}_state.dart"
        read_state_file.write_text(
            get_read_state_template(name), encoding="utf-8"
        )

    if not only_read:
        write_cubit_file = cubit_path / f"write_{plural_name}_cubit.dart"
        write_cubit_file.write_text(
            get_write_cubit_template(
                name,
                reactive,
                import_prefix,
                business_package,
            ),
            encoding="utf-8",
        )

        write_state_file = cubit_path / f"write_{plural_name}_state.dart"
        write_state_file.write_text(
            get_write_state_template(name), encoding="utf-8"
        )

    if reactive and not business_package:
        ensure_reactive_repository(output_dir)

    Mediator().output_folders.append(str(cubit_path))
