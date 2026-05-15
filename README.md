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

#### `onion crud-mongo`

Creates a CRUD module (router + controller + repository + datasource + model) **plus a MongoDB collection** and service.

```bash
onion crud-mongo <NAME> [<NAME> ...] --version <VERSION>
```

Generates everything from `crud` plus:
- `app/services/mongo_service.py`
- `app/services/mongo_collections/v{version}/{plural_name}_collection.py`
- `app/config/onion-config.toml`

| Argument/Option | Description |
|---|---|
| `NAME` | Entity name(s) in singular |
| `--version` | **Required.** API version number |

#### `onion repo`

Creates a **repository module** (repository + datasource + model) with no router/controller.

```bash
onion repo <NAME> [<NAME> ...] --version <VERSION>
```

Generates:
- `app/repos/v{version}/{plural_name}/{plural_name}_repository.py`
- `app/repos/v{version}/{plural_name}/data/{plural_name}_datasource.py`
- `app/repos/v{version}/{plural_name}/models/{single_name}_model.py`

#### `onion repo-mongo`

Creates a repository module **with** a MongoDB collection.

```bash
onion repo-mongo <NAME> [<NAME> ...] --version <VERSION>
```

#### `onion router`

Creates a **router and controller only** (no repository).

```bash
onion router <NAME> [<NAME> ...] --version <VERSION>
```

Generates:
- `app/api/v{version}/{plural_name}/{plural_name}_router.py`
- `app/api/v{version}/{plural_name}/{plural_name}_controller.py`
- `app/api/v{version}/router.py` (auto-updated with new route includes)

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
- `read_{plural_name}_cubit.dart` + `read_{plural_name}_state.dart`
- `write_{plural_name}_cubit.dart` + `write_{plural_name}_state.dart`

| Option | Description |
|---|---|
| `--read-only` | Generate only read cubit |
| `--write-only` | Generate only write cubit |

#### `onion flutter-module`

Creates a **complete Flutter feature module** with cubits, dialogs, view, and widgets.

```bash
onion flutter-module <NAME> --output-dir "."
```

Generates `lib/src/modules/{plural_name}/` with:
- `cubit/` (read + write cubit and state)
- `dialogs/` (stub file)
- `view/` (stub file)
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
├── api/v{version}/          # Presentation layer (routers/controllers)
├── repos/v{version}/        # Domain layer (repositories, datasources, models)
│   ├── data/                # Data sources (external API calls)
│   └── models/              # Domain models
├── services/                # Infrastructure (MongoDB service, etc.)
│   └── mongo_collections/   # MongoDB collection definitions
└── config/                  # Configuration (onion-config.toml)
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


# Onion CLI — Usage Guide

Onion CLI generates boilerplate code following the **Onion Architecture**. This guide explains every command, the naming conventions, and the expected workflows for both **FastAPI (Python)** and **Flutter (Dart)** projects.

---

## Naming Conventions

All entity names must be provided in **singular** form. The CLI automatically derives 4 name variations:

| Variation | Example (`product`) | Example (`category`) |
|---|---|---|
| `Name` (PascalCase) | `Product` | `Category` |
| `Name_plural` (PascalCase) | `Products` | `Categories` |
| `single_name` (snake_case) | `product` | `category` |
| `plural_name` (snake_case) | `products` | `categories` |

**Rules:**
- Plural names are **rejected** with an error. Use `product` not `products`.
- Hyphens, spaces, and underscores in input are normalized to PascalCase. `order-item` → `OrderItem`.
- The pluralization follows English grammar rules (irregular nouns like `person` → `people`, `leaf` → `leaves`, etc. are handled).

---

## Output Directory & Context

All commands that generate FastAPI code assume the current working directory contains an `app/` folder (or will create one). The project scaffolding commands (`project`) explicitly create the folder structure from templates.

---

## FastAPI Commands

### Scaffolding

#### `onion project fastapi-app`

Copies the `app/` folder from the FastAPI template. Placeholder `example`/`examples` is replaced with your entity name.

```bash
# Inside your project root:
onion project fastapi-app . --force
```

**Structure created:**
```
app/
├── api/v1/examples/
│   ├── examples_controller.py
│   └── examples_router.py
├── repos/v1/examples/
│   ├── data/examples_datasource.py
│   ├── models/example_model.py
│   └── examples_repository.py
├── core/
├── config/
├── services/
├── tools/
└── main.py
```

#### `onion project fastapi-init`

Copies a **complete** FastAPI project (root files, Dockerfile, tests, configs, etc.).

```bash
onion project fastapi-init ./my-new-project
```

**Structure created:**
```
my-new-project/
├── app/           (same as fastapi-app above)
├── test/
├── Dockerfile
├── pyproject.toml
├── .dockerignore
├── .gitignore
└── runtime.txt
```

---

### CRUD Generation

There are 3 tiers of CRUD generation. Choose the one that fits your needs:

| Command | Router + Controller | Repo + Datasource + Model | Mongo Collection |
|---|---|---|---|
| `router` | ✅ | ❌ | ❌ |
| `crud` | ✅ | ✅ | ❌ |
| `repo` | ❌ | ✅ | ❌ |
| `crud-mongo` | ✅ | ✅ | ✅ |
| `repo-mongo` | ❌ | ✅ | ✅ |

All CRUD commands accept one or more entity names. The `--version` flag is **required**.

```bash
# Single entity
onion crud product --version 1

# Multiple entities at once
onion crud product category supplier --version 1
```

#### `onion crud`

Creates router, controller, repository, datasource, and model.

```bash
onion crud product --version 1
```

**Generated files:**
```
app/
├── api/v1/products/
│   ├── products_router.py        # FastAPI router with CRUD endpoints
│   ├── products_controller.py    # Controller wired to repository
│   └── __init__.py
└── repos/v1/products/
    ├── products_repository.py    # Repository (singleton, calls datasource)
    ├── data/products_datasource.py  # Data source (stub to implement)
    ├── models/product_model.py   # Pydantic models: BaseProduct, CreateProduct, UpdateProduct, ProductInDb
    └── __init__.py               # Re-exports all classes
```

The version router `app/api/v1/router.py` is also auto-created/updated with `include_router()` lines.

**Number of files created:** 6

#### `onion router`

Creates **only** the router and controller (no repository layer).

```bash
onion router product --version 1
```

**Generated files:**
```
app/api/v1/products/
├── products_router.py       # Router with Any types (no typed models)
├── products_controller.py   # Basic controller with NotImplementedError stubs
└── __init__.py
```

**Use case:** For endpoints that don't need a database (e.g., health checks, external API proxies).

**Number of files created:** 2 (+ auto-update to `router.py`)

#### `onion repo`

Creates **only** the repository layer (no router/controller).

```bash
onion repo product --version 1
```

**Generated files:**
```
app/repos/v1/products/
├── products_repository.py
├── data/products_datasource.py
├── models/product_model.py
└── __init__.py
```

**Use case:** When you need the data layer but want to wire the router manually.

**Number of files created:** 4

#### `onion crud-mongo`

Full CRUD + MongoDB collection + MongoDB service.

```bash
onion crud-mongo product --version 1
```

**Generated files:** Everything from `crud` plus:
```
app/services/
├── mongo_service.py                       # Singleton MongoDB client (Motor)
└── mongo_collections/v1/
    ├── products_collection.py             # Collection class with CRUD operations
    └── __init__.py
app/config/
└── onion-config.toml                      # Tracks registered collections
```

The datasource is wired to use the MongoDB collection (instead of leaving NotImplementedError).

**Number of files created:** 9

#### `onion repo-mongo`

Repository layer + MongoDB collection (no router/controller).

```bash
onion repo-mongo product --version 1
```

**Generated files:** Everything from `repo` plus `mongo_service.py`, `mongo_collections/v1/products_collection.py`, and `onion-config.toml`.

**Number of files created:** 7

---

### Generated Code Structure (FastAPI)

#### Router (`products_router.py`)

```python
@products_router.post("")           # POST /products
@products_router.get("")            # GET /products
@products_router.get("/{product_id}")   # GET /products/{product_id}
@products_router.patch("/{product_id}") # PATCH /products/{product_id}
@products_router.delete("/{product_id}")# DELETE /products/{product_id}
```

When generated via `crud` or `crud-mongo`, endpoints are fully typed with `CreateProduct`, `UpdateProduct`, `ProductInDb`. With `router` alone, they use `Any`.

#### Controller (`products_controller.py`)

Wired to the repository via singleton pattern. Delegates all calls to `ProductsRepository`.

#### Repository (`products_repository.py`)

Singleton with `get_instance()`. Calls the datasource and validates results into Pydantic models.

#### Datasource (`products_datasource.py`)

- Without MongoDB: stub with `NotImplementedError`.
- With MongoDB: calls `ProductsCollection` methods.

#### Model (`product_model.py`)

```python
class BaseProduct(BaseModel): pass     # Common fields
class CreateProduct(BaseProduct): pass # POST body
class UpdateProduct(BaseModel): pass   # PATCH body
class ProductInDb(BaseProduct):        # Response (id, created_at, updated_at)
```

#### Version Router (`app/api/v1/router.py`)

Auto-generated with `include_router()` for each module.

---

## Dart / Flutter Commands

All Dart commands assume you are inside a Flutter project.

### `onion dart`

Generates model + datasource + repository for one entity.

```bash
# Inside a Flutter project:
onion dart product
```

**Generated files:**
```
lib/src/
├── models/product_model.dart              # BaseProduct, CreateProduct, UpdateProduct, ProductInDb
├── data/
│   ├── products_data_source.dart          # Data source (HttpService) with full CRUD+search
│   └── data_sources.dart                  # Barrel file
└── domain/repositories/
    ├── products_repository.dart           # Repository with local caching
    └── repositories.dart                  # Barrel file
```

**Number of files created:** 5

**Default output:** `./lib/src`. Override with `--output-dir`.

### `onion dart-model`

Creates model classes only.

```bash
onion dart-model product --output-dir "./lib/src"
```

**Generated:**
```
lib/src/models/product_model.dart
```

Contains 4 classes: `BaseProduct`, `CreateProduct`, `UpdateProduct`, `ProductInDb`.

### `onion dart-cubit`

Creates cubit + state files for Flutter Bloc state management.

```bash
# Create both read and write cubits (default):
onion dart-cubit product

# Read-only:
onion dart-cubit product --read-only

# Write-only:
onion dart-cubit product --write-only
```

**Generated:** `{output_dir}/{name}_cubit/` with:
- `read_products_cubit.dart` + `read_products_state.dart`
- `write_products_cubit.dart` + `write_products_state.dart`

**States (Read):** `ReadProductInitial`, `ReadProductLoading`, `ReadProductSuccess` (with lists for items/new/updated/deleted), `ReadProductSearching`, `HighlightedProductItem`, `ReadProductError`.

**States (Write):** `WriteProductInitial`, `WritingProduct`, `WriteProductSuccess`, `ProductCreated`, `ProductUpdated`, `ProductDeleted`, `WriteProductError`.

### `onion flutter-module`

Creates a complete feature module folder structure.

```bash
onion flutter-module product
```

**Generated:** `lib/src/modules/products/` with:
```
cubit/
├── read_products_cubit.dart
├── read_products_state.dart
├── write_products_cubit.dart
└── write_products_state.dart
dialogs/products_dialogs.dart      # Stub
view/products_view.dart            # Stub
widgets/products_widgets.dart      # Stub
```

**Number of files created:** 6

### `onion barrel`

Creates a Dart barrel file (re-export) for any directory.

```bash
# Re-export all .dart files in lib/src/models:
onion barrel ./lib/src/models --filename export.dart
```

**Generated:** `{directory}/export.dart` with `export '...';` lines for every `.dart` file.

---

### Generated Code Structure (Dart)

#### Data Source (`products_data_source.dart`)

Singleton with `HttpService` mixin. Endpoints:
- `POST /products` → `createProduct()`
- `GET /products` → `getAllProducts()`
- `GET /products/{id}` → `getProductById()`
- `GET /products/search/{keyword}` → `searchProductByKeyword()`
- `PATCH /products/{id}` → `updateProductById()`
- `DELETE /products/{id}` → `deleteProductById()`

#### Repository (`products_repository.dart`)

Wraps the data source, maintains an in-memory `_products` list. Adds:
- `searchByKeywordLocal()` — client-side filtering on cached data
- Automatic list update after create/update/delete

#### Models (`product_model.dart`)

4 classes: `BaseProduct`, `CreateProduct`, `UpdateProduct`, `ProductInDb` (with `fromJson`).

---

## Flutter Project Scaffolding

### `onion project flutter-lib`

Copies the Flutter template and replaces placeholder names.

```bash
onion project flutter-lib ./my-flutter-app --package "com.company.app" --force
```

**What is replaced:**
- `sample` → your entity name (snake_case)
- `Sample` → PascalCase
- `sample_entity` / `SampleEntity` → derived variations
- `kardex_app_front` → package name (with dots replaced by underscores)

Filenames containing `sample`/`Sample` are also renamed.

---

## Workflows

### Typical FastAPI Project Setup

```bash
# 1. Initialize a complete FastAPI project
onion project fastapi-init ./my-api

# 2. Generate CRUD for entities
cd ./my-api
onion crud product --version 1
onion crud category --version 1
onion crud-mongo order --version 1   # if using MongoDB

# 3. Implement the datasource logic
# Edit: app/repos/v1/products/data/products_datasource.py
# Edit: app/repos/v1/categories/data/categories_datasource.py
```

### Typical Flutter Project Setup

```bash
# 1. Initialize Flutter template
onion project flutter-lib ./my-app --package "com.company.app"

# 2. Generate data layer for entities
cd ./my-app
onion dart product
onion dart category

# 3. Generate cubits for state management
onion dart-cubit product
onion dart-cubit category

# 4. Or generate a complete module at once
onion flutter-module product
```

### Adding a New Entity to an Existing Project

```bash
# FastAPI with plain CRUD:
onion crud supplier --version 1

# FastAPI with MongoDB:
onion crud-mongo supplier --version 1

# FastAPI, data layer only:
onion repo supplier --version 1

# FastAPI, endpoints only:
onion router supplier --version 1
```

---

## Summary File Counts

| Command | Files Created | Category |
|---|---|---|
| `project fastapi-app` | ~15 | Scaffolding |
| `project fastapi-init` | ~25 | Scaffolding |
| `project flutter-lib` | ~20 | Scaffolding |
| `crud` | 6 | CRUD |
| `crud-mongo` | 9 | CRUD + Mongo |
| `repo` | 4 | Data Layer |
| `repo-mongo` | 7 | Data Layer + Mongo |
| `router` | 2 | Endpoints |
| `dart` | 5 | Dart Data Layer |
| `dart-model` | 1 | Dart Model |
| `dart-cubit` | 4 | Dart State |
| `flutter-module` | 6 | Dart Module |
| `barrel` | 1 | Utility |
