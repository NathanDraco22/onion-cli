from pathlib import Path

from onion.mediators import Mediator
from onion.templates.dart.view_template import (
    get_responsive_body_template,
    get_view_template,
)
from onion.utils.dart.extensions_util import ensure_extensions
from onion.utils.dart.pubspec_util import require_pubspec_name
from onion.utils.dart.reactive_repo_util import find_package_root
from onion.utils.string_utils import get_entity_name_variations


def create_view(
    input_name: str,
    output_dir: str = ".",
    responsive: bool = False,
    providers: bool = False,
    business_package: str | None = None,
) -> None:
    variations = get_entity_name_variations(input_name)
    plural_name = variations.plural_name

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    app_package: str | None = None
    if responsive or providers:
        app_package = require_pubspec_name(find_package_root(output_dir))

    view_file = output_path / f"{plural_name}_screen.dart"
    view_file.write_text(
        get_view_template(
            input_name,
            responsive=responsive,
            providers=providers,
            app_package=app_package,
            business_package=business_package,
        ),
        encoding="utf-8",
    )
    Mediator().output_folders.append(str(view_file))

    if responsive:
        ensure_extensions(output_dir)
        for variant in ("mobile", "tablet", "desktop"):
            variant_dir = output_path / variant
            variant_dir.mkdir(parents=True, exist_ok=True)
            variant_file = variant_dir / f"{plural_name}_screen_{variant}.dart"
            variant_file.write_text(
                get_responsive_body_template(input_name, variant),
                encoding="utf-8",
            )
            Mediator().output_folders.append(str(variant_file))
