import importlib
from inspect import getmodule
from itertools import starmap, chain
from types import ModuleType
from typing import Callable, Dict, Any, Optional, Tuple
from warnings import warn

from ._get_dynamic_classes import _get_dynamic_classes
from ..classes.DynamicClassCreator import DynamicClassCreator


def _re_import_dynamic_classes(
    module_name: str, dynamic_classes: Dict[str, Dict[str, DynamicClassCreator]]
) -> ModuleType:
    """
    Updates instances of dynamic class that are imported from the module.
    :param module_name: Name of the module which classes are re-imported.
    :param dynamic_classes: Dictionary of all dynamic classes divided on modules.
    :return: Re-imported module.
    """
    re_imported_module = importlib.import_module(module_name)
    for variable, dynamic_class in dynamic_classes.get(module_name, {}).items():
        new_class = getattr(re_imported_module, variable)
        for instance in dynamic_class._instances:
            instance.__class__ = new_class
        new_class._instances = dynamic_class._instances
    return re_imported_module


def _get_module_variable(
    module: ModuleType, locals_: Dict, variable: str
) -> Optional[str]:
    """
    Gets a module variable that has the same value as a value of given variable in a local scope.
    Used when import as is used to recover corresponding variable name from the module.
    :param module: A module to search the variable in.
    :param locals_: A dictionary of local variables.
    :param variable: A variable name.
    :return: A corresponding variables name from the module.
    """
    if hasattr(module, variable):
        return variable
    return next(
        chain.from_iterable(
            (
                (
                    var
                    for var in dir(module)
                    if locals_[variable] == getattr(module, var)
                ),
                [None],
            )
        )
    )


def _re_import_modules(modules: Dict[str, ModuleType], locals_: Dict, globals_: Dict):
    """
    Re-imports specified module and updates local and global variables with changed values.

    :param modules: A dictionary of a (module name, module) pairs.
    :param locals_: local variables typically locals().
    :param globals_: global variables typically globals().
    """

    def get_valid_module(key: str, value: Any) -> Optional[Tuple[str, ModuleType]]:
        """
        Gets an origin module of a given value if the value is not callable (these need no update).

        :param key: A variable name.
        :param value: Any value to be matched.
        :return: A pair of (key, the original module of the value) or None
        """
        if not isinstance(value, Callable):
            return
        module = getmodule(value)
        if module not in modules.values():
            return
        return key, module

    locals_from_modules = dict(filter(None, starmap(get_valid_module, locals_.items())))
    globals_from_modules = dict(
        filter(None, starmap(get_valid_module, globals_.items()))
    )
    local_modules = dict(
        (key, value)
        for key, value in locals_.items()
        if isinstance(value, ModuleType) and key != "__builtins__"
    )
    global_modules = dict(
        (key, value)
        for key, value in globals_.items()
        if isinstance(value, ModuleType) and key != "__builtins__"
    )
    local_as_translations = dict(
        filter(
            lambda item: item[1] is not None,
            (
                (variable, _get_module_variable(module, locals_, variable))
                for variable, module in locals_from_modules.items()
            ),
        )
    )
    global_as_translations = dict(
        filter(
            lambda item: item[1] is not None,
            (
                (variable, _get_module_variable(module, globals_, variable))
                for variable, module in globals_from_modules.items()
            ),
        )
    )
    dynamic_classes = dict(
        (module_name, _get_dynamic_classes(module))
        for module_name, module in modules.items()
    )
    for value in modules.values():
        try:
            importlib.reload(value)
        except Exception as e:
            warn(f"Dynamic executor wasn't able to fully reload {e}")
    local_modules = dict(
        (variable, _re_import_dynamic_classes(module.__name__, dynamic_classes))
        for variable, module in local_modules.items()
    )
    global_modules = dict(
        (variable, _re_import_dynamic_classes(module.__name__, dynamic_classes))
        for variable, module in global_modules.items()
    )
    locals_from_modules = dict(
        (
            variable,
            getattr(
                _re_import_dynamic_classes(module.__name__, dynamic_classes),
                local_as_translations[variable],
            ),
        )
        for variable, module in locals_from_modules.items()
    )
    globals_from_modules = dict(
        (
            variable,
            getattr(
                _re_import_dynamic_classes(module.__name__, dynamic_classes),
                global_as_translations[variable],
            ),
        )
        for variable, module in globals_from_modules.items()
    )
    for variable, value in locals_from_modules.items():
        locals_[variable] = value
    for variable, value in globals_from_modules.items():
        globals_[variable] = value
    for variable, module in local_modules.items():
        locals_[variable] = module
    for variable, module in global_modules.items():
        globals_[variable] = module
