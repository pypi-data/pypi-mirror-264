""""Import module"""

import importlib


class ModelImportError(Exception):
    """Exception raised when an error occures when importing a model class"""


def get_variable(module_name: str, variable_name: str):
    """Returns a variable from a module

    Args:
        module_name (str)
        variable_name (str)
    """

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        raise ModelImportError(f"Could not find module {module_name}") from e

    return getattr(module, variable_name)
