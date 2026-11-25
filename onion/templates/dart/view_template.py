from onion.utils.string_utils import get_entity_name_variations


def get_view_template(
    singular_name: str,
    responsive: bool = False,
    providers: bool = False,
    app_package: str | None = None,
    business_package: str | None = None,
) -> str:
    if not singular_name or not isinstance(singular_name, str):
        raise ValueError("name is not a valid string")

    variations = get_entity_name_variations(singular_name)
    name = variations.Name
    name_plural = variations.Name_plural
    plural_name = variations.plural_name

    if providers and not app_package:
        raise ValueError("app_package is required to generate providers")
    if responsive and not app_package:
        raise ValueError("app_package is required to generate responsive views")

    imports = ["import 'package:flutter/material.dart';"]

    if providers:
        imports.append("import 'package:flutter_bloc/flutter_bloc.dart';")
        imports.append(
            f"import 'package:{app_package}/src/cubits/{plural_name}/"
            f"read_{plural_name}_cubit.dart';"
        )
        imports.append(
            f"import 'package:{app_package}/src/cubits/{plural_name}/"
            f"write_{plural_name}_cubit.dart';"
        )
        if business_package:
            imports.append(
                f"import 'package:{business_package}/{business_package}.dart';"
            )
        else:
            imports.append(
                f"import 'package:{app_package}/src/domain/repositories/"
                f"{plural_name}_repository.dart';"
            )

    if responsive:
        imports.append(
            f"import 'package:{app_package}/src/tools/extensiones.dart';"
        )

    parts: list[str] = []
    if responsive:
        parts = [
            f"part 'mobile/{plural_name}_screen_mobile.dart';",
            f"part 'tablet/{plural_name}_screen_tablet.dart';",
            f"part 'desktop/{plural_name}_screen_desktop.dart';",
        ]

    if providers:
        screen_build = f"""    return MultiBlocProvider(
      providers: [
        BlocProvider(
          create: (ctx) => Read{name}Cubit(
            RepositoryProvider.of<{name_plural}Repository>(ctx),
          )..getAll(),
        ),
        BlocProvider(
          create: (ctx) => Write{name}Cubit(
            RepositoryProvider.of<{name_plural}Repository>(ctx),
          ),
        ),
      ],
      child: const _RootScaffold(),
    );"""
    else:
        screen_build = "    return const _RootScaffold();"

    if responsive:
        body_build = f"""    if (context.isMobile()) return const _{name_plural}MobileBody();
    if (context.isTablet()) return const _{name_plural}TabletBody();
    return const _{name_plural}DesktopBody();"""
    else:
        body_build = f"""    return const Center(
      child: Text('{name_plural}Screen'),
    );"""

    header = "\n".join(imports)
    if parts:
        header += "\n\n" + "\n".join(parts)

    return f"""{header}

class {name_plural}Screen extends StatelessWidget {{
  const {name_plural}Screen({{super.key}});

  @override
  Widget build(BuildContext context) {{
{screen_build}
  }}
}}

class _RootScaffold extends StatelessWidget {{
  const _RootScaffold();

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(title: const Text('{name_plural}')),
      body: const _Body(),
    );
  }}
}}

class _Body extends StatelessWidget {{
  const _Body();

  @override
  Widget build(BuildContext context) {{
{body_build}
  }}
}}
"""


def get_responsive_body_template(singular_name: str, variant: str) -> str:
    if not singular_name or not isinstance(singular_name, str):
        raise ValueError("name is not a valid string")
    if variant not in {"mobile", "tablet", "desktop"}:
        raise ValueError("variant must be mobile, tablet or desktop")

    variations = get_entity_name_variations(singular_name)
    name_plural = variations.Name_plural
    plural_name = variations.plural_name
    variant_class = variant.capitalize()
    class_name = f"_{name_plural}{variant_class}Body"

    return f"""part of '../{plural_name}_screen.dart';

class {class_name} extends StatelessWidget {{
  const {class_name}({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return const Center(
      child: Text('{name_plural} {variant}'),
    );
  }}
}}
"""
