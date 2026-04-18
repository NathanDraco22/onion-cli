from onion.utils.string_utils import get_entity_name_variations


def get_repository_template(singular_name: str) -> str:
    if not singular_name or not isinstance(singular_name, str):
        raise ValueError("name is not a valid string")

    variations = get_entity_name_variations(singular_name)

    name = variations.Name
    name_plural = variations.Name_plural
    plural_name = variations.plural_name
    single_name = variations.single_name
    single_name_id = single_name + "Id"

    return (
        "\n"
        "class " + name_plural + "Repository {\n"
        "  final " + name_plural + "DataSource " + plural_name + "DataSource;\n"
        "\n"
        "  " + name_plural + "Repository(this." + plural_name + "DataSource);\n"
        "\n"
        "  List<" + name + "InDb> _" + plural_name + " = [];\n"
        "\n"
        "  List<" + name + "InDb> get " + plural_name + " => _" + plural_name + ";\n"
        "\n"
        "  Future<"
        + name
        + "InDb> create"
        + name
        + "(Create"
        + name
        + " create"
        + name
        + ") async {\n"
        "    final result = await "
        + plural_name
        + "DataSource.create"
        + name
        + "(create"
        + name
        + ".toJson());\n"
        "    final new" + name + " = " + name + "InDb.fromJson(result);\n"
        "    _" + plural_name + " = [new" + name + ", ..._" + plural_name + "];\n"
        "    return new" + name + ";\n"
        "  }\n"
        "\n"
        "  Future<List<" + name + "InDb>> getAll" + name_plural + "() async {\n"
        "    final results = await "
        + plural_name
        + "DataSource.getAll"
        + name_plural
        + "();\n"
        "    final response = ListResponse<" + name + "InDb>.fromJson(\n"
        "      results,\n"
        "      " + name + "InDb.fromJson,\n"
        "    );\n"
        "\n"
        "    _" + plural_name + " = response.data;\n"
        "    _" + plural_name + ".sort(\n"
        "      (a, b) => a.name.toLowerCase().compareTo(b.name.toLowerCase()),\n"
        "    );\n"
        "    return _" + plural_name + ";\n"
        "  }\n"
        "\n"
        "  Future<"
        + name
        + "InDb?> get"
        + name
        + "ById(String "
        + single_name_id
        + ") async {\n"
        "    final result = await "
        + plural_name
        + "DataSource.get"
        + name
        + "ById("
        + single_name_id
        + ");\n"
        "    if (result == null) return null;\n"
        "    return " + name + "InDb.fromJson(result);\n"
        "  }\n"
        "\n"
        "  Future<List<"
        + name
        + "InDb>> search"
        + name
        + "ByKeyword(String keyword) async {\n"
        "    final result = await "
        + plural_name
        + "DataSource.search"
        + name
        + "ByKeyword(keyword);\n"
        "    final response = ListResponse<" + name + "InDb>.fromJson(\n"
        "      result,\n"
        "      " + name + "InDb.fromJson,\n"
        "    );\n"
        "    return response.data;\n"
        "  }\n"
        "\n"
        "  Future<List<"
        + name
        + "InDb>> search"
        + name
        + "ByKeywordLocal(String keyword) async {\n"
        "    final result = " + plural_name + "\n"
        "        .where(\n"
        "          (u) => u.name.toLowerCase().contains(\n"
        "            keyword.toLowerCase(),\n"
        "          ),\n"
        "        )\n"
        "        .toList();\n"
        "    return result;\n"
        "  }\n"
        "\n"
        "  Future<" + name + "InDb?> update" + name + "ById(\n"
        "    String " + single_name_id + ",\n"
        "    Update" + name + " " + single_name + ",\n"
        "  ) async {\n"
        "    final result = await "
        + plural_name
        + "DataSource.update"
        + name
        + "ById(\n"
        "      " + single_name_id + ",\n"
        "      " + single_name + ".toJson(),\n"
        "    );\n"
        "    if (result == null) return null;\n"
        "\n"
        "    final updated" + name + " = " + name + "InDb.fromJson(result);\n"
        "    final index = _"
        + plural_name
        + ".indexWhere((u) => u.id == "
        + single_name_id
        + ");\n"
        "    if (index != -1) {\n"
        "      _" + plural_name + "[index] = updated" + name + ";\n"
        "    }\n"
        "    return updated" + name + ";\n"
        "  }\n"
        "\n"
        "  Future<"
        + name
        + "InDb?> delete"
        + name
        + "ById(String "
        + single_name_id
        + ") async {\n"
        "    final result = await "
        + plural_name
        + "DataSource.delete"
        + name
        + "ById("
        + single_name_id
        + ");\n"
        "    if (result == null) return null;\n"
        "\n"
        "    final deleted" + name + " = " + name + "InDb.fromJson(result);\n"
        "    _" + plural_name + ".removeWhere((u) => u.id == " + single_name_id + ");\n"
        "    return deleted" + name + ";\n"
        "  }\n"
        "}\n"
    )
