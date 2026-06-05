from pathlib import Path
from onion.mediators import Mediator
from onion.templates.dart.service_templates import (
    get_http_service_template,
    get_http_exceptions_template,
    get_hive_service_template,
)


def create_service(services_str: str, output_dir: str = ".") -> None:
    services = [s.strip().lower() for s in services_str.split(",") if s.strip()]
    if not services:
        raise Exception("No services specified")

    output_path = Path(output_dir)

    for service in services:
        if service == "http":
            if not output_path.exists():
                output_path.mkdir(parents=True)

            http_file = output_path / "http_service.dart"
            http_file.write_text(get_http_service_template())
            Mediator().output_folders.append(str(http_file))

            exceptions_path = output_path / "exceptions"
            if not exceptions_path.exists():
                exceptions_path.mkdir(parents=True)

            exceptions_file = exceptions_path / "http_exceptions.dart"
            exceptions_file.write_text(get_http_exceptions_template())
            Mediator().output_folders.append(str(exceptions_file))

        elif service == "hive":
            if not output_path.exists():
                output_path.mkdir(parents=True)

            hive_file = output_path / "hive_service.dart"
            hive_file.write_text(get_hive_service_template())
            Mediator().output_folders.append(str(hive_file))

        else:
            raise Exception(
                f"Service type '{service}' is not supported. Supported types: 'http', 'hive'"
            )
