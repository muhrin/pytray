import contextlib

__all__ = ('capture_exceptions',)


@contextlib.contextmanager
def capture_exceptions(future, ignore=()):
    """
    Capture any uncaught exceptions in the context and set them as the result of the given future

    :param future: The future to the exception on, has to have a `set_exception()` method
    :param ignore: An optional list of exception types to ignore, these will be raised and not set on the future
    """
    try:
        yield
    except Exception as exception:  # pylint: disable=broad-except
        if isinstance(exception, ignore):
            raise

        future.set_exception(exception)
