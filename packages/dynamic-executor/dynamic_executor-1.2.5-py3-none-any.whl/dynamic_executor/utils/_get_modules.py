import inspect
import sys
import platform
from types import ModuleType
from typing import Dict

venv_module = (
    f"python{'.'.join(sys.version.split('.')[:2])}"
    if platform.system() == "Linux"
    else f"Python{''.join(sys.version.split('.')[:2])}"
)


def _get_modules() -> Dict[str, ModuleType]:
    """
    Collects all imported module except these connected with dynamic_executor.

    :return: Dictionary of (module_name, module) pairs.
    """
    return dict(
        (variable, value)
        for variable, value in sys.modules.items()
        if getattr(value, "__file__", None) is not None
        and venv_module not in inspect.getfile(value)
        and "pycharm-professional" not in inspect.getfile(value)
        and not variable.startswith("_")
    )
