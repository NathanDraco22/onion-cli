from onion.utils.string_utils import get_entity_name_variations


def get_read_cubit_template(singular_name: str) -> str:
    if not singular_name or not isinstance(singular_name, str):
        raise ValueError("name is not a valid string")

    variations = get_entity_name_variations(singular_name)

    name = variations.Name
    name_plural = variations.Name_plural
    plural_name = variations.plural_name
    single_name = variations.single_name
    single_name_id = single_name + "Id"

    return (
        "import 'package:flutter_bloc/flutter_bloc.dart';\n"
        "import 'package:" + single_name + "_model.dart';\n"
        "\n"
        "part 'read_" + plural_name + "_state.dart';\n"
        "\n"
        "class Read" + name + "Cubit extends Cubit<Read" + name + "State> {\n"
        "  Read" + name + "Cubit() : super(Read" + name + "Initial());\n"
        "\n"
        "  Future<void> getAll() async {\n"
        "    emit(Read" + name + "Loading());\n"
        "    // TODO: implement getAll\n"
        "  }\n"
        "\n"
        "  Future<void> getById(String " + single_name_id + ") async {\n"
        "    emit(Read" + name + "Loading());\n"
        "    // TODO: implement getById\n"
        "  }\n"
        "\n"
        "  void mark" + name + "Updated(" + name + " item) {\n"
        "    final currentState = state;\n"
        "    if (currentState is Read" + name + "Success) {\n"
        "      final updatedItems = [...currentState.updatedItems, item];\n"
        "      emit(Read"
        + name
        + "Success(currentState.items, updatedItems: updatedItems));\n"
        "    }\n"
        "  }\n"
        "\n"
        "  void put" + name + "First(" + name + " item) {\n"
        "    final currentState = state;\n"
        "    if (currentState is Read" + name + "Success) {\n"
        "      final items = [item, ...currentState.items.where((u) => u.id != item.id)];\n"
        "      emit(Read" + name + "Success(items, updatedItems: [item]));\n"
        "    }\n"
        "  }\n"
        "}\n"
    )


def get_read_state_template(singular_name: str) -> str:
    if not singular_name or not isinstance(singular_name, str):
        raise ValueError("name is not a valid string")

    variations = get_entity_name_variations(singular_name)

    name = variations.Name
    plural_name = variations.plural_name

    return (
        "part of 'read_" + plural_name + "_cubit.dart';\n"
        "\n"
        "sealed class Read" + name + "State {}\n"
        "\n"
        "final class Read" + name + "Initial extends Read" + name + "State {}\n"
        "\n"
        "final class Read" + name + "Loading extends Read" + name + "State {}\n"
        "\n"
        "class Read" + name + "Success extends Read" + name + "State {\n"
        "  final List<" + name + "> items;\n"
        "  List<" + name + "> newItems;\n"
        "  List<" + name + "> updatedItems;\n"
        "  List<" + name + "> deletedItems;\n"
        "\n"
        "  Read" + name + "Success(\n"
        "    this.items, {\n"
        "    this.newItems = const [],\n"
        "    this.updatedItems = const [],\n"
        "    this.deletedItems = const [],\n"
        "  });\n"
        "}\n"
        "\n"
        "final class Read" + name + "Searching extends Read" + name + "Success {\n"
        "  Read" + name + "Searching(\n"
        "    super.items, {\n"
        "    super.newItems,\n"
        "    super.updatedItems,\n"
        "    super.deletedItems,\n"
        "  });\n"
        "}\n"
        "\n"
        "class Highlighted" + name + "Item extends Read" + name + "Success {\n"
        "  Highlighted" + name + "Item(\n"
        "    super.items, {\n"
        "    super.newItems,\n"
        "    super.updatedItems,\n"
        "    super.deletedItems,\n"
        "  });\n"
        "}\n"
        "\n"
        "final class Read" + name + "Error extends Read" + name + "State {\n"
        "  final String message;\n"
        "  Read" + name + "Error(this.message);\n"
        "}\n"
    )
