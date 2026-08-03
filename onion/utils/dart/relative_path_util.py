from pathlib import Path


def get_relative_prefix(from_dir: Path, package_root: Path) -> str:
    target = package_root / "lib" / "src"
    rel = from_dir.resolve().relative_to(target.resolve())
    return "../" * len(rel.parts)
