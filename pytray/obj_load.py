"""Module for methods used to load objects/symbols dynamically in python"""
from typing import Union
import types

__version__ = "0.0.1"

__all__ = '__version__', 'load_obj', 'full_name'


def load_obj(name: str) -> Union[type, types.FunctionType, types.BuiltinFunctionType]:
    """Load a type from a fully qualified name"""
    components = name.split('.')
    mod = __import__(components[0])
    # Get the components one by one
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def full_name(symbol: Union[type, types.FunctionType, types.BuiltinFunctionType]) -> str:
    """Get the fully qualified name of a type.
    """
    return symbol.__module__ + '.' + symbol.__name__
