from pathlib import Path

from onion.mediators import Mediator
from onion.utils.dart.reactive_repo_util import find_package_root

EXTENSIONS_TEMPLATE = """import 'package:flutter/widgets.dart';

// Responsive breakpoints.
// TODO: move these constants to the business package when available.
const maxPhoneScreenWidth = 600;
const maxTabletScreenWidth = 840;

extension BuildContextExtension on BuildContext {
  bool isMobile() => MediaQuery.sizeOf(this).width < maxPhoneScreenWidth;

  bool isTablet() {
    final width = MediaQuery.sizeOf(this).width;
    return width >= maxPhoneScreenWidth && width < maxTabletScreenWidth;
  }

  bool isDesktop() => MediaQuery.sizeOf(this).width >= maxTabletScreenWidth;

  bool isMobileOrTablet() =>
      MediaQuery.sizeOf(this).width < maxTabletScreenWidth;

  bool isTabletOrDesktop() =>
      MediaQuery.sizeOf(this).width >= maxPhoneScreenWidth;
}
"""


def ensure_extensions(output_dir: str) -> str:
    """Create lib/src/tools/extensiones.dart if it does not exist.

    The generated responsive screen imports this file. It is idempotent: an
    existing file is never overwritten.
    """
    package_root = find_package_root(output_dir)
    if not (package_root / "pubspec.yaml").exists():
        raise ValueError(
            "No pubspec.yaml found. Responsive views require a Flutter app root."
        )

    file_path = package_root / "lib" / "src" / "tools" / "extensiones.dart"
    if file_path.exists():
        return str(file_path)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(EXTENSIONS_TEMPLATE, encoding="utf-8")
    Mediator().output_folders.append(str(file_path))
    return str(file_path)
