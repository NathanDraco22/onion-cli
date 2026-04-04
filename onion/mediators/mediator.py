class Mediator:
    """
    This class is a mediator between the cli and the onion generator.
    It is a singleton and it is used to call the methods of the cli
    from the onion generator.
    """

    _instance: "Mediator|None" = None

    def __new__(cls) -> "Mediator":
        if cls._instance is None:
            cls._instance = super(Mediator, cls).__new__(cls)
        return cls._instance

    output_folders: list[str] = []
