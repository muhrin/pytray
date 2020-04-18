"""Pretty printing functions"""

import typing

import deprecation

from .version import __version__


def type_string(obj_type: typing.Type) -> str:
    """Given an type will return a simple type string"""
    type_str = str(obj_type)
    if type_str.startswith('<class '):
        return type_str[8:-2]
    return type_str


@deprecation.deprecated(deprecated_in="0.2.1",
                        removed_in="0.3.0",
                        current_version=__version__,
                        details="Use type_string() instead")
def pretty_type_string(obj_type: typing.Type) -> str:
    return type_string(obj_type)
