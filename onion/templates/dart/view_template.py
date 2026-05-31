from onion.utils.string_utils import get_entity_name_variations


def get_view_template(singular_name: str) -> str:
    if not singular_name or not isinstance(singular_name, str):
        raise ValueError("name is not a valid string")

    variations = get_entity_name_variations(singular_name)
    name_plural = variations.Name_plural

    return (
        "import 'package:flutter/material.dart';\n"
        "\n"
        f"class {name_plural}Screen extends StatelessWidget {{\n"
        f"  const {name_plural}Screen({{super.key}});\n"
        "\n"
        "  @override\n"
        "  Widget build(BuildContext context) {\n"
        "    return const _RootScaffold();\n"
        "  }\n"
        "}\n"
        "\n"
        "class _RootScaffold extends StatelessWidget {\n"
        "  const _RootScaffold();\n"
        "\n"
        "  @override\n"
        "  Widget build(BuildContext context) {\n"
        "    return const Scaffold(\n"
        "      body: _Body(),\n"
        "    );\n"
        "  }\n"
        "}\n"
        "\n"
        "class _Body extends StatelessWidget {\n"
        "  const _Body();\n"
        "\n"
        "  @override\n"
        "  Widget build(BuildContext context) {\n"
        "    return const Center(\n"
        f'      child: Text("{name_plural}Screen"),\n'
        "    );\n"
        "  }\n"
        "}\n"
    )
