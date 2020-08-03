import enum
import re
from pytray import obj_load


def test_load_class():
    # Test with a class
    name = obj_load.full_name(enum.Enum)
    assert name == 'enum.Enum'
    obj_type = obj_load.load_obj(name)
    assert obj_type is enum.Enum

    # Now test loading something that we haven't imported the module for
    obj_type = obj_load.load_obj('argparse.ArgumentParser')
    import argparse  # pylint: disable=import-outside-toplevel
    assert obj_type is argparse.ArgumentParser

    # Test with builtin
    name = obj_load.full_name(dict)
    obj_load.load_obj(name)


def test_load_function():
    name = obj_load.full_name(re.match)
    assert name == 're.match'
    assert obj_load.load_obj(name) is re.match
