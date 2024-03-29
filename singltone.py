"""
File with singletone meta-class.
"""

class MetaSingleton(type):
    """
    Meta-class implementing the singleton pattern.

    Returns:
        cls: Class object instance.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
