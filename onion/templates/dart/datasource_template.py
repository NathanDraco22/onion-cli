from onion.utils.string_utils import get_entity_name_variations


def get_datasource_template(singular_name: str) -> str:
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
        "class " + name_plural + "DataSource with HttpService {\n"
        "  " + name_plural + "DataSource._();\n"
        "  static final "
        + name_plural
        + "DataSource instance = "
        + name_plural
        + "DataSource._();\n"
        "  factory " + name_plural + "DataSource() {\n"
        "    return instance;\n"
        "  }\n"
        "\n"
        '  final _endpoint = "/' + plural_name + '";\n'
        "\n"
        "  Future<Map<String, dynamic>> create"
        + name
        + "(Map<String, dynamic> "
        + single_name
        + ") async {\n"
        "    final uri = HttpTools.generateUri(_endpoint);\n"
        "    final headers = HttpTools.generateAuthHeaders();\n"
        "    final res = await postQuery(uri, " + single_name + ", headers: headers);\n"
        "    return res;\n"
        "  }\n"
        "\n"
        "  Future<Map<String, dynamic>> getAll" + name_plural + "() async {\n"
        "    final uri = HttpTools.generateUri(_endpoint);\n"
        "    final headers = HttpTools.generateAuthHeaders();\n"
        "    final res = await getQuery(uri, headers: headers);\n"
        "    return res;\n"
        "  }\n"
        "\n"
        "  Future<Map<String, dynamic>?> get"
        + name
        + "ById(String "
        + single_name_id
        + ") async {\n"
        '    final uri = HttpTools.generateUri(_endpoint + "/" + '
        + single_name_id
        + ");\n"
        "    final headers = HttpTools.generateAuthHeaders();\n"
        "    final res = await getQuery(uri, headers: headers);\n"
        "    return res;\n"
        "  }\n"
        "\n"
        "  Future<Map<String, dynamic>> search"
        + name
        + "ByKeyword(String keyword) async {\n"
        '    final uri = HttpTools.generateUri(_endpoint + "/search/" + keyword);\n'
        "    final headers = HttpTools.generateAuthHeaders();\n"
        "    final res = await getQuery(uri, headers: headers);\n"
        "    return res;\n"
        "  }\n"
        "\n"
        "  Future<Map<String, dynamic>?> update" + name + "ById(\n"
        "    String " + single_name_id + ",\n"
        "    Map<String, dynamic> " + single_name + ",\n"
        "  ) async {\n"
        '    final uri = HttpTools.generateUri(_endpoint + "/" + '
        + single_name_id
        + ");\n"
        "    final headers = HttpTools.generateAuthHeaders();\n"
        "    final res = await patchQuery(uri, body: "
        + single_name
        + ", headers: headers);\n"
        "    return res;\n"
        "  }\n"
        "\n"
        "  Future<Map<String, dynamic>?> delete"
        + name
        + "ById(String "
        + single_name_id
        + ") async {\n"
        '    final uri = HttpTools.generateUri(_endpoint + "/" + '
        + single_name_id
        + ");\n"
        "    final headers = HttpTools.generateAuthHeaders();\n"
        "    final res = await deleteQuery(uri, headers: headers);\n"
        "    return res;\n"
        "  }\n"
        "}\n"
    )
