def get_fully_qualified_class_name(cls):
    """
    Get the fully qualified class name of a class.

    Args:
        cls: The class.

    Returns:
        The fully qualified class name.
    """
    return cls.__module__ + "." + cls.__class__.__qualname__
