from pytray import tree


def test_flattening():
    my_tree = {
        'a': {
            'b': 6,
            'c': 'potato'
        },
        'd': [{
            'e': [],
        }, 'hello']
    }
    flattened = tree.flatten(my_tree)
    assert flattened.pop(('a', 'b')) == 6
    assert flattened.pop(('a', 'c')) == 'potato'
    assert flattened.pop(('d', 0, 'e')) == []
    assert flattened.pop(('d', 1)) == 'hello'
    assert not flattened


def test_flattening_filter():
    my_tree = {'a': {'b': 5, 'c': {'d': 6}}}
    # Don't flatten {'d': 6}
    flattened = tree.flatten(my_tree, filter=lambda value: value != {'d': 6})
    assert flattened.pop(('a', 'b')) == 5
    assert flattened.pop(('a', 'c')) == {'d': 6}
    assert not flattened


def test_path_to_string():
    pathstring = tree.path_to_string(('a', 'b', 'c', 0, 'd'))
    assert pathstring == "a.b.c.0.d"
