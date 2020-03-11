import collections
import collections.abc
import typing
import weakref


class WeakObjectIdDict(collections.MutableMapping):
    """
    Like weakref.WeakKeyDict but internally uses object ids instead of the object reference
    itself thereby avoiding the need for the object to be hashable (and therefore immutable).
    """

    def __init__(self, seq=None, **kwargs):
        self._refs = {}  # type: collections.abc.MutableMapping[int, weakref.ReferenceType]
        self._values = {}  # type: collections.abc.MutableMapping[int, typing.Any]
        if seq:
            if isinstance(seq, collections.abc.Mapping):
                for key, value in seq.items():
                    self[key] = value
            elif isinstance(seq, collections.Iterable):
                for key, value in seq:
                    self[key] = value
        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def __copy__(self):
        return WeakObjectIdDict(self)

    def __getitem__(self, item):
        try:
            return self._values[id(item)]
        except KeyError:
            raise KeyError(str(item))

    def __setitem__(self, key, value):
        obj_id = id(key)
        wref = weakref.ref(key, self._finalised)
        self._refs[obj_id] = wref
        self._values[obj_id] = value

    def __delitem__(self, key):
        obj_id = id(key)
        del self._values[obj_id]
        del self._refs[obj_id]

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        for ref in self._refs.values():
            yield ref()

    def _finalised(self, wref):
        found_id = None
        for obj_id, ref in self._refs.items():
            if ref == wref:
                found_id = obj_id
                break
        # Delete both the object values and the reference itself
        del self._values[found_id]
        del self._refs[found_id]
