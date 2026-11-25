# Contexto de Conversación con Gemini

## v0.8.0 — Flutter responsive y alcance de cubits

- **`dart-cubit`**: genera `{output_dir}/{plural_name}/` (antes `{name}_cubit/`); nuevo flag `--business-package` para importar `package:{name}/{name}.dart`.
- **`dart-view`**: genera `{plural_name}_screen.dart` (antes `_view.dart`); nuevo flag `--responsive` con variantes `mobile/`, `tablet/`, `desktop/` y `extensiones.dart`.
- **`flutter-module`**: los cubits van a `lib/src/cubits/{plural_name}/` (fuera del módulo); el screen queda en `view/{plural_name}_screen.dart` con `MultiBlocProvider`; flags `--responsive` y `--business-package`.
- **Tests**: `test/test_dart_generators.py` con pytest; `testpaths = ["test"]` para no recolectar el template FastAPI.
- **Versión**: `0.7.3` → `0.8.0`.

## Comando Agregado: `onion dart-service`

Se ha implementado el comando `onion dart-service` en la CLI de `onion-cli` para facilitar la creación de servicios de infraestructura `http` y `hive` en proyectos Dart/Flutter.

### Archivos Creados/Modificados:
1.  **`onion/templates/dart/service_templates.py` (Nuevo):** Contiene los strings de plantilla para `HttpService`, `HttpServiceException` y `HiveService`.
2.  **`onion/actions/dart/create_service.py` (Nuevo):** Implementa la lógica para validar qué servicios se solicitaron (separados por coma), escribir los archivos correspondientes en el directorio de salida y registrar los archivos en el `Mediator` de la CLI.
3.  **`onion/main.py` (Modificado):** Registra el nuevo comando `dart-service` en la CLI usando Typer.

### Funcionamiento del Comando:
*   Acepta los tipos de servicio como un argumento (por ejemplo: `http`, `hive`, o `http,hive`).
*   Acepta la opción `--output-dir` para cambiar el destino por defecto (que es el directorio de trabajo `.`).
*   Si se solicita `http`, genera `http_service.dart` y `exceptions/http_exceptions.dart`.
*   Si se solicita `hive`, genera `hive_service.dart`.


## Comando Agregado: `onion dart-res`

Se ha implementado el comando `onion dart-res` para generar la respuesta estática genérica `ListResponse` en Dart/Flutter.

### Archivos Creados/Modificados/Eliminados:
1.  **`onion/templates/dart/response_template.py` (Nuevo):** Contiene la plantilla de la clase `ListResponse<T>`.
2.  **`onion/actions/dart/create_response.py` (Nuevo):** Lógica para escribir el archivo `list_response.dart` en el destino de salida y registrarlo en el Mediator.
3.  **`onion/main.py` (Modificado):** Registra el comando `dart-res` en la CLI usando Typer.
4.  **`onion/fixed_files/` (Eliminado):** Se eliminó por completo el directorio de archivos fijos de servicios en Dart.
5.  **`onion/project_base/flutter_app/` (Eliminado):** Se eliminó la plantilla de aplicación Flutter completa.
6.  **`onion/actions/project/copy_flutter_project.py` (Eliminado):** Se eliminó la acción de copia de Flutter.
7.  **`onion/main.py` (Modificado):** Se eliminó el comando `flutter-lib` (bajo el subcomando `project`).

### Funcionamiento de `onion dart-res`:
*   Genera el archivo `list_response.dart` en el directorio de salida especificado (por defecto es el directorio actual `.`).
