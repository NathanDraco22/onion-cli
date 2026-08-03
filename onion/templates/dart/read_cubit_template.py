from onion.utils.string_utils import get_entity_name_variations


def get_read_cubit_template(
    singular_name: str,
    reactive: bool = False,
    import_prefix: str = "../../",
) -> str:
    if not singular_name or not isinstance(singular_name, str):
        raise ValueError("name is not a valid string")

    variations = get_entity_name_variations(singular_name)

    name = variations.Name
    name_plural = variations.Name_plural
    plural_name = variations.plural_name
    single_name = variations.single_name
    single_name_id = single_name + "Id"

    model_import = (
        "import '"
        + import_prefix
        + "domain/models/"
        + single_name
        + "_model/"
        + single_name
        + "_model.dart';\n"
    )
    repo_import = (
        "import '"
        + import_prefix
        + "domain/repositories/"
        + plural_name
        + "_repository.dart';\n"
    )

    if reactive:
        return (
            "import 'dart:async';\n"
            "\n"
            "import 'package:flutter_bloc/flutter_bloc.dart';\n"
            "\n"
            + model_import
            + repo_import
            + "import '"
            + import_prefix
            + "tools/reactive_repo/reactive_repository.dart';\n"
            "\n"
            "part 'read_" + plural_name + "_state.dart';\n"
            "\n"
            "class Read" + name + "Cubit extends Cubit<Read" + name + "State> {\n"
            "  Read" + name + "Cubit(this._repository) : super(Read" + name + "Initial()) {\n"
            "    _subscription = _repository.eventStream.listen(_handleRepoEvent);\n"
            "  }\n"
            "\n"
            "  final " + name_plural + "Repository _repository;\n"
            "  StreamSubscription<RepoEvent<" + name + "InDb>>? _subscription;\n"
            "\n"
            "  Future<void> getAll() async {\n"
            "    final currentState = state;\n"
            "    if (currentState is Read" + name + "Success) {\n"
            "      emit(Read" + name + "Refreshing.fromSuccess(currentState));\n"
            "    } else {\n"
            "      emit(Read" + name + "Loading());\n"
            "    }\n"
            "    try {\n"
            "      final items = await _repository.getAll" + name_plural + "();\n"
            "      emit(Read" + name + "Success(items));\n"
            "    } catch (error) {\n"
            "      emit(Read" + name + "Error(error.toString()));\n"
            "    }\n"
            "  }\n"
            "\n"
            "  Future<void> getById(String " + single_name_id + ") async {\n"
            "    emit(Read" + name + "Loading());\n"
            "    try {\n"
            "      final item = await _repository.get" + name + "ById(" + single_name_id + ");\n"
            "      if (item == null) {\n"
            "        emit(Read" + name + "Error(\"" + name + " not found\"));\n"
            "      } else {\n"
            "        emit(Read" + name + "Success([item]));\n"
            "      }\n"
            "    } catch (error) {\n"
            "      emit(Read" + name + "Error(error.toString()));\n"
            "    }\n"
            "  }\n"
            "\n"
            "  void _handleRepoEvent(RepoEvent<" + name + "InDb> event) {\n"
            "    switch (event) {\n"
            "      case RepoItemCreated(:final item):\n"
            "        mark" + name + "Created(item);\n"
            "      case RepoItemUpdated(:final item):\n"
            "        mark" + name + "Updated(item);\n"
            "      case RepoItemDeleted(:final item):\n"
            "        mark" + name + "Deleted(item);\n"
            "    }\n"
            "  }\n"
            "\n"
            "  void mark" + name + "Created(" + name + "InDb item) {\n"
            "    final currentState = state;\n"
            "    if (currentState is Read" + name + "Success) {\n"
            "      final items = [item, ...currentState.items.where((u) => u.id != item.id)];\n"
            "      final newItems = [...currentState.newItems, item];\n"
            "      emit(Read"
            + name
            + "Success(items, newItems: newItems));\n"
            "    }\n"
            "  }\n"
            "\n"
            "  void mark" + name + "Updated(" + name + "InDb item) {\n"
            "    final currentState = state;\n"
            "    if (currentState is Read" + name + "Success) {\n"
            "      final items = currentState.items.map((u) => u.id == item.id ? item : u).toList();\n"
            "      final updatedItems = [...currentState.updatedItems, item];\n"
            "      emit(Read"
            + name
            + "Success(items, updatedItems: updatedItems));\n"
            "    }\n"
            "  }\n"
            "\n"
            "  void mark" + name + "Deleted(" + name + "InDb item) {\n"
            "    final currentState = state;\n"
            "    if (currentState is Read" + name + "Success) {\n"
            "      final deletedItems = [...currentState.deletedItems, item];\n"
            "      emit(Read"
            + name
            + "Success(currentState.items, deletedItems: deletedItems));\n"
            "    }\n"
            "  }\n"
            "\n"
            "  @override\n"
            "  Future<void> close() async {\n"
            "    _subscription?.cancel();\n"
            "    await super.close();\n"
            "  }\n"
            "}\n"
        )

    return (
        "import 'package:flutter_bloc/flutter_bloc.dart';\n"
        "\n"
        + model_import
        + repo_import
        + "part 'read_" + plural_name + "_state.dart';\n"
        "\n"
        "class Read" + name + "Cubit extends Cubit<Read" + name + "State> {\n"
        "  Read" + name + "Cubit(this._repository) : super(Read" + name + "Initial());\n"
        "\n"
        "  final " + name_plural + "Repository _repository;\n"
        "\n"
        "  Future<void> getAll() async {\n"
        "    final currentState = state;\n"
        "    if (currentState is Read" + name + "Success) {\n"
        "      emit(Read" + name + "Refreshing.fromSuccess(currentState));\n"
        "    } else {\n"
        "      emit(Read" + name + "Loading());\n"
        "    }\n"
        "    try {\n"
        "      final items = await _repository.getAll" + name_plural + "();\n"
        "      emit(Read" + name + "Success(items));\n"
        "    } catch (error) {\n"
        "      emit(Read" + name + "Error(error.toString()));\n"
        "    }\n"
        "  }\n"
        "\n"
        "  Future<void> getById(String " + single_name_id + ") async {\n"
        "    emit(Read" + name + "Loading());\n"
        "    try {\n"
        "      final item = await _repository.get" + name + "ById(" + single_name_id + ");\n"
        "      if (item == null) {\n"
        "        emit(Read" + name + "Error(\"" + name + " not found\"));\n"
        "      } else {\n"
        "        emit(Read" + name + "Success([item]));\n"
        "      }\n"
        "    } catch (error) {\n"
        "      emit(Read" + name + "Error(error.toString()));\n"
        "    }\n"
        "  }\n"
        "\n"
        "  void mark" + name + "Created(" + name + "InDb item) {\n"
        "    final currentState = state;\n"
        "    if (currentState is Read" + name + "Success) {\n"
        "      final items = [item, ...currentState.items.where((u) => u.id != item.id)];\n"
        "      final newItems = [...currentState.newItems, item];\n"
        "      emit(Read"
        + name
        + "Success(items, newItems: newItems));\n"
        "    }\n"
        "  }\n"
        "\n"
        "  void mark" + name + "Updated(" + name + "InDb item) {\n"
        "    final currentState = state;\n"
        "    if (currentState is Read" + name + "Success) {\n"
        "      final items = currentState.items.map((u) => u.id == item.id ? item : u).toList();\n"
        "      final updatedItems = [...currentState.updatedItems, item];\n"
        "      emit(Read"
        + name
        + "Success(items, updatedItems: updatedItems));\n"
        "    }\n"
        "  }\n"
        "\n"
        "  void mark" + name + "Deleted(" + name + "InDb item) {\n"
        "    final currentState = state;\n"
        "    if (currentState is Read" + name + "Success) {\n"
        "      final deletedItems = [...currentState.deletedItems, item];\n"
        "      emit(Read"
        + name
        + "Success(currentState.items, deletedItems: deletedItems));\n"
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
        "  final List<" + name + "InDb> items;\n"
        "  List<" + name + "InDb> newItems;\n"
        "  List<" + name + "InDb> updatedItems;\n"
        "  List<" + name + "InDb> deletedItems;\n"
        "\n"
        "  Read" + name + "Success(\n"
        "    this.items, {\n"
        "    this.newItems = const [],\n"
        "    this.updatedItems = const [],\n"
        "    this.deletedItems = const [],\n"
        "  });\n"
        "}\n"
        "\n"
        "final class Read" + name + "Refreshing extends Read" + name + "Success {\n"
        "  Read" + name + "Refreshing(\n"
        "    super.items, {\n"
        "    super.newItems,\n"
        "    super.updatedItems,\n"
        "    super.deletedItems,\n"
        "  });\n"
        "\n"
        "  factory Read" + name + "Refreshing.fromSuccess(\n"
        "    Read" + name + "Success success,\n"
        "  ) =>\n"
        "      Read" + name + "Refreshing(\n"
        "        success.items,\n"
        "        newItems: success.newItems,\n"
        "        updatedItems: success.updatedItems,\n"
        "        deletedItems: success.deletedItems,\n"
        "      );\n"
        "}\n"
        "\n"
        "final class Read" + name + "Error extends Read" + name + "State {\n"
        "  final String message;\n"
        "  Read" + name + "Error(this.message);\n"
        "}\n"
    )
