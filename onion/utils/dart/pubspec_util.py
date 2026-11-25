import re
from pathlib import Path


def get_pubspec_name(package_root: Path) -> str | None:
    """Read the package name from a Flutter/Dart pubspec.yaml.

    The CLI avoids adding a YAML dependency; the `name` field is a simple
    top-level scalar and can be read with a regex.
    """
    pubspec = package_root / "pubspec.yaml"
    if not pubspec.exists():
        return None

    for line in pubspec.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(
            r"^\s*name:\s*['\"]?([A-Za-z0-9_]+)['\"]?\s*$",
            line,
        )
        if match:
            return match.group(1)

    return None


def require_pubspec_name(package_root: Path) -> str:
    name = get_pubspec_name(package_root)
    if not name:
        raise ValueError(
            "No pubspec.yaml with a valid 'name' was found. "
            "Run the command from a Flutter/Dart app root."
        )
    return name
