from types import ModuleType
from typing import Dict
from warnings import warn

from ..classes.DynamicClassCreator import DynamicClassCreator


def _get_dynamic_classes(module: ModuleType) -> Dict[str, DynamicClassCreator]:
    """Collects all dynamic classes from a module.

    :param module: A module to collect classes from.
    :return: A dictionary of (variable name, dynamic_class instance) pairs.
    """
    out_dictionary = {}
    for variable in dir(module):
        try:
            if getattr(module, variable) in DynamicClassCreator.created_classes:
                out_dictionary[variable] = getattr(module, variable)
        except Exception as e:
            warn(f"Dynamic executor wasn't able to fully reload {e}")
    return out_dictionary
