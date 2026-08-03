from onion.utils.string_utils import get_entity_name_variations


def get_write_cubit_template(
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
            "import 'package:flutter_bloc/flutter_bloc.dart';\n"
            "\n"
            + model_import
            + repo_import
            + "part 'write_" + plural_name + "_state.dart';\n"
            "\n"
            "class Write" + name + "Cubit extends Cubit<Write" + name + "State> {\n"
            "  Write" + name + "Cubit(this._repository) : super(Write" + name + "Initial());\n"
            "\n"
            "  final " + name_plural + "Repository _repository;\n"
            "\n"
            "  Future<void> create(Create" + name + " create" + name + ") async {\n"
            "    emit(Writing" + name + "());\n"
            "    try {\n"
            "      final item = await _repository.create" + name + "(create" + name + ");\n"
            "      emit(" + name + "Created(item));\n"
            "      emit(Write" + name + "Initial());\n"
            "    } catch (error) {\n"
            "      emit(Write" + name + "Error(error.toString()));\n"
            "    }\n"
            "  }\n"
            "\n"
            "  Future<void> update(String "
            + single_name_id
            + ", Update"
            + name
            + " "
            + single_name
            + ") async {\n"
            "    emit(Writing" + name + "());\n"
            "    try {\n"
            "      final item = await _repository.update" + name + "ById("
            + single_name_id
            + ", "
            + single_name
            + ");\n"
            "      if (item == null) {\n"
            "        emit(Write" + name + "Error(\"" + name + " not found\"));\n"
            "      } else {\n"
            "        emit(" + name + "Updated(item));\n"
            "        emit(Write" + name + "Initial());\n"
            "      }\n"
            "    } catch (error) {\n"
            "      emit(Write" + name + "Error(error.toString()));\n"
            "    }\n"
            "  }\n"
            "\n"
            "  Future<void> delete(String " + single_name_id + ") async {\n"
            "    emit(Writing" + name + "());\n"
            "    try {\n"
            "      final item = await _repository.delete" + name + "ById(" + single_name_id + ");\n"
            "      if (item == null) {\n"
            "        emit(Write" + name + "Error(\"" + name + " not found\"));\n"
            "      } else {\n"
            "        emit(" + name + "Deleted(item));\n"
            "        emit(Write" + name + "Initial());\n"
            "      }\n"
            "    } catch (error) {\n"
            "      emit(Write" + name + "Error(error.toString()));\n"
            "    }\n"
            "  }\n"
            "}\n"
        )

    return (
        "import 'package:flutter_bloc/flutter_bloc.dart';\n"
        "\n"
        + model_import
        + repo_import
        + "part 'write_" + plural_name + "_state.dart';\n"
        "\n"
        "class Write" + name + "Cubit extends Cubit<Write" + name + "State> {\n"
        "  Write" + name + "Cubit(this._repository) : super(Write" + name + "Initial());\n"
        "\n"
        "  final " + name_plural + "Repository _repository;\n"
        "\n"
        "  Future<void> create(Create" + name + " create" + name + ") async {\n"
        "    emit(Writing" + name + "());\n"
        "    try {\n"
        "      final item = await _repository.create" + name + "(create" + name + ");\n"
        "      emit(" + name + "Created(item));\n"
        "      emit(Write" + name + "Initial());\n"
        "    } catch (error) {\n"
        "      emit(Write" + name + "Error(error.toString()));\n"
        "    }\n"
        "  }\n"
        "\n"
        "  Future<void> update(String "
        + single_name_id
        + ", Update"
        + name
        + " "
        + single_name
        + ") async {\n"
        "    emit(Writing" + name + "());\n"
        "    try {\n"
        "      final item = await _repository.update" + name + "ById("
        + single_name_id
        + ", "
        + single_name
        + ");\n"
        "      if (item == null) {\n"
        "        emit(Write" + name + "Error(\"" + name + " not found\"));\n"
        "      } else {\n"
        "        emit(" + name + "Updated(item));\n"
        "        emit(Write" + name + "Initial());\n"
        "      }\n"
        "    } catch (error) {\n"
        "      emit(Write" + name + "Error(error.toString()));\n"
        "    }\n"
        "  }\n"
        "\n"
        "  Future<void> delete(String " + single_name_id + ") async {\n"
        "    emit(Writing" + name + "());\n"
        "    try {\n"
        "      final item = await _repository.delete" + name + "ById(" + single_name_id + ");\n"
        "      if (item == null) {\n"
        "        emit(Write" + name + "Error(\"" + name + " not found\"));\n"
        "      } else {\n"
        "        emit(" + name + "Deleted(item));\n"
        "        emit(Write" + name + "Initial());\n"
        "      }\n"
        "    } catch (error) {\n"
        "      emit(Write" + name + "Error(error.toString()));\n"
        "    }\n"
        "  }\n"
        "}\n"
    )


def get_write_state_template(singular_name: str) -> str:
    if not singular_name or not isinstance(singular_name, str):
        raise ValueError("name is not a valid string")

    variations = get_entity_name_variations(singular_name)

    name = variations.Name
    plural_name = variations.plural_name

    return (
        "part of 'write_" + plural_name + "_cubit.dart';\n"
        "\n"
        "sealed class Write" + name + "State {}\n"
        "\n"
        "final class Write" + name + "Initial extends Write" + name + "State {}\n"
        "\n"
        "final class Writing" + name + " extends Write" + name + "State {}\n"
        "\n"
        "class Write" + name + "Success extends Write" + name + "State {\n"
        "  final " + name + "InDb item;\n"
        "  Write" + name + "Success(this.item);\n"
        "}\n"
        "\n"
        "final class " + name + "Created extends Write" + name + "Success {\n"
        "  " + name + "Created(super.item);\n"
        "}\n"
        "\n"
        "final class " + name + "Updated extends Write" + name + "Success {\n"
        "  " + name + "Updated(super.item);\n"
        "}\n"
        "\n"
        "final class " + name + "Deleted extends Write" + name + "Success {\n"
        "  " + name + "Deleted(super.item);\n"
        "}\n"
        "\n"
        "final class Write" + name + "Error extends Write" + name + "State {\n"
        "  final String message;\n"
        "  Write" + name + "Error(this.message);\n"
        "}\n"
    )
