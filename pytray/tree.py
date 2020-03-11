"""A tree in this context is considered a nested container containing either lists or
dictionaries and with anything else being considered a leaf.  Paths to particular points
in the data structure are represented as sequences containing the index at each level"""
from functools import reduce
import operator


def get_by_path(root, items):
    """Access a nested object in root by item sequence.  Taken from:
    https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys"""
    if not items:
        # Support either empty items or None items meaning give back root
        return root
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence.  Taken from:
    https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys"""
    get_by_path(root, items[:-1])[items[-1]] = value


def path_to_string(path: tuple) -> str:
    return ".".join((str(key) for key in path))


def transform(visitor, root, path: tuple = (), **kwargs):
    """Given a list or a dict call create a new container of that type calling
    `visitor` for each entry to get the transformed value.  kwargs will be passed
    to the visitor.
    """

    if isinstance(root, dict):
        return {key: visitor(value, path=path + (key,), **kwargs) for key, value in root.items()}
    if isinstance(root, list):
        return [visitor(value, path=path + (idx,), **kwargs) for idx, value in enumerate(root)]

    return root


def flatten(root, filter=None) -> dict:  # pylint: disable=redefined-builtin
    """Given a tree flatten it into a dictionary contaning the path as key and the corresponding
    leaves as values"""

    def should_flatten(value):
        return (isinstance(value, (dict, list)) and bool(value)) \
               and (filter is None or filter(value))

    def do_flattening(entry, path=()):
        if should_flatten(entry):
            # Descend further
            if isinstance(entry, dict):
                for key, value in entry.items():
                    yield from do_flattening(value, path + (key,))
            elif isinstance(entry, list):
                for idx, value in enumerate(entry):
                    yield from do_flattening(value, path + (idx,))
            else:
                raise TypeError("Cannot flatten type '{}'".format(type(entry)))
        else:
            yield path, entry

    return dict(do_flattening(root))
