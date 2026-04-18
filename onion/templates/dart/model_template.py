from onion.utils.string_utils import get_entity_name_variations


def get_model_template(singular_name: str) -> str:
    if not singular_name or not isinstance(singular_name, str):
        raise ValueError("name is not a valid string")

    variations = get_entity_name_variations(singular_name)

    name = variations.Name
    name_plural = variations.Name_plural
    single_name = variations.single_name

    return (
        "class Base" + name + " extends Base" + name + "{\n"
        "  final String id;\n"
        "\n"
        "  Base" + name + "({required this.id});\n"
        "}\n"
        "\n"
        "class Create" + name + " {\n"
        "  Map<String, dynamic> toJson() {\n"
        "    return {};\n"
        "  }\n"
        "}\n"
        "\n"
        "class Update" + name + " {\n"
        "  Map<String, dynamic> toJson() {\n"
        "    return {};\n"
        "  }\n"
        "}\n"
        "\n"
        "class " + name + "InDb extends Base" + name + " {\n"
        "  " + name + "InDb({required super.id});\n"
        "\n"
        "  factory " + name + "InDb.fromJson(Map<String, dynamic> json) {\n"
        "    return " + name + "InDb(\n"
        "      id: json['id'] as String,\n"
        "    );\n"
        "  }\n"
        "}\n"
    )
