from pathlib import Path
from onion.mediators import Mediator
from onion.templates.mongo_service_template import get_mongo_service_template
from onion.templates.base_mongo_collection_template import (
    get_base_mongo_collection_template,
)
from onion.utils.file_utils import gen_init


def create_mongo_service():
    print("Creating mongo service...")
    # check "app" folder
    app_folder = Path("app")
    if not app_folder.exists():
        app_folder.mkdir()

    # check "app/services" folder
    service_folder = app_folder / "services"
    if not service_folder.exists():
        service_folder.mkdir()

    # check "app/services/mongo_service.py"
    service_file = service_folder / "mongo_service.py"
    if not service_file.exists():
        service_file.touch()

    service_file.write_text(get_mongo_service_template())

    # check "app/services/base_mongo_collection.py"
    base_collection_file = service_folder / "base_mongo_collection.py"
    if not base_collection_file.exists():
        base_collection_file.touch()

    base_collection_file.write_text(get_base_mongo_collection_template())

    gen_init(service_folder)

    Mediator().output_folders.append("app/services/mongo_service.py")
    Mediator().output_folders.append("app/services/base_mongo_collection.py")
