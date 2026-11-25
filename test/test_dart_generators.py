from pathlib import Path

import pytest

from onion.actions.dart.create_cubit import create_cubit
from onion.actions.dart.create_flutter_module import create_flutter_module
from onion.actions.dart.create_view import create_view
from onion.mediators import Mediator


@pytest.fixture(autouse=True)
def reset_mediator():
    Mediator().output_folders.clear()
    yield
    Mediator().output_folders.clear()


@pytest.fixture
def app(tmp_path: Path) -> Path:
    root = tmp_path / "demo_app"
    (root / "lib" / "src").mkdir(parents=True)
    (root / "pubspec.yaml").write_text("name: demo_app\n", encoding="utf-8")
    return root


def test_cubit_uses_plural_folder_and_business_imports(app: Path) -> None:
    create_cubit(
        "product",
        str(app / "lib" / "src" / "cubits"),
        business_package="demo_business",
    )

    cubit_dir = app / "lib" / "src" / "cubits" / "products"
    assert (cubit_dir / "read_products_cubit.dart").exists()
    assert (cubit_dir / "write_products_cubit.dart").exists()
    assert not (app / "lib" / "src" / "cubits" / "product_cubit").exists()

    read_content = (cubit_dir / "read_products_cubit.dart").read_text(
        encoding="utf-8"
    )
    assert "package:demo_business/demo_business.dart" in read_content
    assert "class ReadProductCubit" in read_content
    assert "../../domain" not in read_content


def test_cubit_uses_relative_imports_without_business_package(app: Path) -> None:
    create_cubit("product", str(app / "lib" / "src" / "cubits"))

    read_content = (
        app
        / "lib"
        / "src"
        / "cubits"
        / "products"
        / "read_products_cubit.dart"
    ).read_text(encoding="utf-8")

    assert "../../domain/models/product_model/product_model.dart" in read_content
    assert "../../domain/repositories/products_repository.dart" in read_content
    assert "class ReadProductCubit" in read_content


def test_responsive_view_generates_screen_parts_and_providers(app: Path) -> None:
    create_view(
        "product",
        str(app / "lib" / "src" / "modules" / "products" / "view"),
        responsive=True,
        providers=True,
        business_package="demo_business",
    )

    view_dir = app / "lib" / "src" / "modules" / "products" / "view"
    screen = view_dir / "products_screen.dart"
    assert screen.exists()
    assert (view_dir / "mobile" / "products_screen_mobile.dart").exists()
    assert (view_dir / "tablet" / "products_screen_tablet.dart").exists()
    assert (view_dir / "desktop" / "products_screen_desktop.dart").exists()
    assert (app / "lib" / "src" / "tools" / "extensiones.dart").exists()

    content = screen.read_text(encoding="utf-8")
    assert "part 'mobile/products_screen_mobile.dart';" in content
    assert "MultiBlocProvider(" in content
    assert "ReadProductCubit(" in content
    assert "WriteProductCubit(" in content
    assert "package:demo_app/src/cubits/products/read_products_cubit.dart" in content
    assert "package:demo_business/demo_business.dart" in content
    assert "context.isMobile()" in content

    mobile = (view_dir / "mobile" / "products_screen_mobile.dart").read_text(
        encoding="utf-8"
    )
    assert "part of '../products_screen.dart';" in mobile
    assert "class _ProductsMobileBody" in mobile


def test_flutter_module_keeps_cubits_outside_the_module(app: Path) -> None:
    create_flutter_module(
        "product",
        str(app / "lib" / "src" / "modules"),
        responsive=True,
        business_package="demo_business",
    )

    module = app / "lib" / "src" / "modules" / "products"
    assert (module / "view" / "products_screen.dart").exists()
    assert not (module / "cubit").exists()
    assert (app / "lib" / "src" / "cubits" / "products" / "read_products_cubit.dart").exists()
    assert (module / "dialogs" / "products_dialogs.dart").exists()
    assert (module / "widgets" / "products_widgets.dart").exists()


def test_simple_view_has_no_parts(app: Path) -> None:
    create_view(
        "product",
        str(app / "lib" / "src" / "modules" / "products" / "view"),
    )

    view_dir = app / "lib" / "src" / "modules" / "products" / "view"
    content = (view_dir / "products_screen.dart").read_text(encoding="utf-8")
    assert "class ProductsScreen" in content
    assert "part '" not in content
    assert not (view_dir / "mobile").exists()


def test_responsive_view_without_providers(app: Path) -> None:
    create_view(
        "product",
        str(app / "lib" / "src" / "modules" / "products" / "view"),
        responsive=True,
    )

    view_dir = app / "lib" / "src" / "modules" / "products" / "view"
    content = (view_dir / "products_screen.dart").read_text(encoding="utf-8")
    assert "part 'mobile/products_screen_mobile.dart';" in content
    assert "context.isTablet()" in content
    assert "MultiBlocProvider(" not in content


def test_flutter_module_without_business_package_uses_app_repository(
    app: Path,
) -> None:
    create_flutter_module(
        "product",
        str(app / "lib" / "src" / "modules"),
    )

    screen = (
        app
        / "lib"
        / "src"
        / "modules"
        / "products"
        / "view"
        / "products_screen.dart"
    )
    content = screen.read_text(encoding="utf-8")
    assert (
        "package:demo_app/src/domain/repositories/products_repository.dart"
        in content
    )
