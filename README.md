# Onion CLI

CLI tool for generating boilerplate code following the **Onion Architecture** (Clean Architecture / Hexagonal Architecture) pattern. Supports both **Python (FastAPI)** and **Dart (Flutter)** projects.

Built with [Typer](https://typer.tiangolo.com/).

## Installation

```bash
pip install onion
```

Or clone the repo and install locally:

```bash
git clone <repo-url>
cd onion-cli
pip install .
```

## Usage

```bash
onion --help
```

---

## Commands

### Project Scaffolding

Create complete project structures from predefined templates.

#### `onion project flutter-lib`

Copies the Flutter project template into `lib/`, replacing placeholder names with your entity name.

```bash
onion project flutter-lib [OUTPUT_DIR] --package "com.example.app" --force
```

| Argument/Option | Default | Description |
|---|---|---|
| `OUTPUT_DIR` | `.` | Project directory |
| `--package` | `com.example.app` | Dart package name |
| `--force` | `False` | Overwrite existing `lib/` folder |

#### `onion project fastapi-app`

Copies the FastAPI `app/` template directory, replacing placeholder entity names.

```bash
onion project fastapi-app [OUTPUT_DIR] --force
```

| Argument/Option | Default | Description |
|---|---|---|
| `OUTPUT_DIR` | `.` | Project directory |
| `--force` | `False` | Overwrite existing `app/` folder |

#### `onion project fastapi-init`

Copies a **complete** FastAPI project (root files, configs, tests, etc.) from the template.

```bash
onion project fastapi-init OUTPUT_DIR --force
```

| Argument/Option | Description |
|---|---|
| `OUTPUT_DIR` | **Required.** Target project directory |
| `--force` | Overwrite existing directory |

---

### CRUD Generators (FastAPI)

Generate routers, controllers, repositories, models, and datasources following the onion architecture.

#### `onion crud`

Creates a **router, controller, repository, datasource, and model** for one or more entities.

```bash
onion crud <NAME> [<NAME> ...] --version <VERSION>
```

Generates:
- `app/api/v{version}/{plural_name}/{plural_name}_router.py`
- `app/api/v{version}/{plural_name}/{plural_name}_controller.py`
- `app/repos/v{version}/{plural_name}/{plural_name}_repository.py`
- `app/repos/v{version}/{plural_name}/data/{plural_name}_datasource.py`
- `app/repos/v{version}/{plural_name}/models/{single_name}_model.py`

| Argument/Option | Description |
|---|---|
| `NAME` | Entity name(s) in singular |
| `--version` | **Required.** API version number |
| `--output-dir` | `""` (default: empty, replaces `app/` or `generated_output/`) |

#### `onion crud-mongo`

Creates a CRUD module (router + controller + repository + datasource + model) **plus a MongoDB collection** and service.

```bash
onion crud-mongo <NAME> [<NAME> ...] --version <VERSION>
```

Generates everything from `crud` plus:
- `app/services/mongo_service.py`
- `app/services/base_mongo_collection.py`
- `app/services/mongo_collections/v{version}/{plural_name}_collection.py`
- `app/config/onion-config.toml`

| Argument/Option | Description |
|---|---|
| `NAME` | Entity name(s) in singular |
| `--version` | **Required.** API version number |
| `--output-dir` | `""` (default: empty, replaces `app/` or `generated_output/`) |

#### `onion repo`

Creates a **repository module** (repository + datasource + model) with no router/controller.

```bash
onion repo <NAME> [<NAME> ...] --version <VERSION>
```

Generates:
- `app/repos/v{version}/{plural_name}/{plural_name}_repository.py`
- `app/repos/v{version}/{plural_name}/data/{plural_name}_datasource.py`
- `app/repos/v{version}/{plural_name}/models/{single_name}_model.py`

| Argument/Option | Description |
|---|---|
| `NAME` | Entity name(s) in singular |
| `--version` | **Required.** API version number |
| `--output-dir` | `""` (default: empty, replaces `app/` or `generated_output/`) |

#### `onion repo-mongo`

Creates a repository module **with** a MongoDB collection.

```bash
onion repo-mongo <NAME> [<NAME> ...] --version <VERSION>
```

| Argument/Option | Description |
|---|---|
| `NAME` | Entity name(s) in singular |
| `--version` | **Required.** API version number |
| `--output-dir` | `""` (default: empty, replaces `app/` or `generated_output/`) |

#### `onion router`

Creates a **router and controller only** (no repository).

```bash
onion router <NAME> [<NAME> ...] --version <VERSION>
```

Generates:
- `app/api/v{version}/{plural_name}/{plural_name}_router.py`
- `app/api/v{version}/{plural_name}/{plural_name}_controller.py`
- `app/api/v{version}/router.py` (auto-updated with new route includes)

| Argument/Option | Description |
|---|---|
| `NAME` | Entity name(s) in singular |
| `--version` | **Required.** API version number |
| `--output-dir` | `""` (default: empty, replaces `app/` or `generated_output/`) |

---

### Dart / Flutter Generators

Generate Dart code following clean architecture (data source → repository → models → cubits).

#### `onion dart`

Creates a **model, datasource, and repository** for a single Dart entity.

```bash
onion dart <NAME> --output-dir "./lib/src"
```

Generates:
- `{output_dir}/models/{single_name}_model.dart`
- `{output_dir}/data/{plural_name}_data_source.dart`
- `{output_dir}/data/data_sources.dart` (barrel file)
- `{output_dir}/domain/repositories/{plural_name}_repository.dart`
- `{output_dir}/domain/repositories/repositories.dart` (barrel file)

| Argument/Option | Default | Description |
|---|---|---|
| `NAME` | | Entity name (e.g., `product`, `client`) |
| `--output-dir` | `./lib/src` | Project source directory |

#### `onion dart-model`

Creates model classes only.

```bash
onion dart-model <NAME> --output-dir "."
```

Generates `{output_dir}/models/{single_name}_model.dart` with 4 classes:
- `Base{Name}`
- `Create{Name}`
- `Update{Name}`
- `{Name}InDb`

#### `onion dart-cubit`

Creates cubit + state files for Flutter Bloc state management.

```bash
onion dart-cubit <NAME> --output-dir "." --read-only --write-only
```

Generates (inside `{name}_cubit/`):
- `read_{plural_name}_cubit.dart` — with `mark{Name}Created` (puts item first + tracks in newItems), `mark{Name}Updated`, and `mark{Name}Deleted`
- `read_{plural_name}_state.dart` — `Read{Name}Success` with `items`, `newItems`, `updatedItems`, `deletedItems`
- `write_{plural_name}_cubit.dart` + `write_{plural_name}_state.dart`

| Option | Description |
|---|---|
| `--read-only` | Generate only read cubit |
| `--write-only` | Generate only write cubit |

#### `onion dart-view`

Creates a **single view screen** for Flutter (StatelessWidget).

```bash
onion dart-view <NAME> --output-dir "."
```

Generates `{output_dir}/{plural_name}_view.dart` with:
- `{Name}Screen` (public)
- `_RootScaffold` (private)
- `_Body` (private)

| Argument/Option | Default | Description |
|---|---|---|
| `NAME` | | Entity name in singular |
| `--output-dir` | `.` | Output directory |

#### `onion flutter-module`

Creates a **complete Flutter feature module** with cubits, dialogs, view, and widgets.

```bash
onion flutter-module <NAME> --output-dir "."
```

Generates `lib/src/modules/{plural_name}/` with:
- `cubit/` (read + write cubit and state)
- `dialogs/` (stub file)
- `view/` (`{Name}Screen` StatelessWidget)
- `widgets/` (stub file)

#### `onion barrel`

Creates a Dart barrel file (`export.dart`) that re-exports all `.dart` files in a directory.

```bash
onion barrel <DIRECTORY> --filename "export.dart"
```

| Argument/Option | Default | Description |
|---|---|---|
| `DIRECTORY` | | **Required.** Directory to scan |
| `--filename` | `export.dart` | Barrel filename |

---

## Architecture Overview

The generated code follows the **Onion Architecture** with these layers:

```
app/
├── api/v{version}/            # Presentation layer (routers/controllers)
├── repos/v{version}/          # Domain layer (repositories, datasources, models)
│   ├── data/                  # Data sources (external API calls)
│   └── models/                # Domain models
├── services/                  # Infrastructure
│   ├── mongo_service.py       # MongoDB client (Motor singleton)
│   ├── base_mongo_collection.py  # Base collection (singleton + wiring)
│   └── mongo_collections/     # MongoDB collection definitions
└── config/                    # Configuration (onion-config.toml)
```

For Dart/Flutter:

```
lib/src/
├── models/                  # Data models
├── data/                    # Data sources (API layer)
├── domain/repositories/     # Repositories (business logic)
└── modules/{feature}/       # Feature modules
    ├── cubit/               # State management
    ├── dialogs/             # UI dialogs
    ├── view/                # Screens/pages
    └── widgets/             # Reusable widgets
```

## Name Convention

All commands accept entity names in **singular** form and automatically:
1. Convert to PascalCase (`product` → `Product`)
2. Derive snake_case (`product`)
3. Derive plural (`products`)
4. Generate all file/class name variations
Plural names are rejected with an error.