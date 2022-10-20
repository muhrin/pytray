# -*- coding: utf-8 -*-
import asyncio
import concurrent.futures
import contextlib

import pytest

from pytray.aiothreads import LoopScheduler


@pytest.fixture
def loop_scheduler():
    loop = asyncio.new_event_loop()
    loop.set_debug(True)
    with LoopScheduler(loop=loop) as scheduler:
        yield scheduler


async def simple(arg):
    await asyncio.sleep(0.1)
    return arg


def test_simple_await_submit(loop_scheduler):  # pylint: disable=redefined-outer-name
    future = loop_scheduler.await_submit(simple("Done!"))
    assert future.result() == "Done!"


def test_simple_await(loop_scheduler):  # pylint: disable=redefined-outer-name
    result = loop_scheduler.await_(simple("Done!"))
    assert result == "Done!"


def test_async_context(loop_scheduler):  # pylint: disable=redefined-outer-name
    sequence = []

    @contextlib.asynccontextmanager
    async def do_():
        sequence.append("Entered")
        yield 10
        sequence.append("Exiting")

    with loop_scheduler.async_ctx(do_()) as value:
        assert value == 10

    assert sequence == ["Entered", "Exiting"]


def test_async_context_exception(
    loop_scheduler,
):  # pylint: disable=redefined-outer-name
    @contextlib.asynccontextmanager
    async def raises_before_yield():
        raise RuntimeError
        yield

    with pytest.raises(RuntimeError):
        with loop_scheduler.async_ctx(raises_before_yield()):
            pass

    @contextlib.asynccontextmanager
    async def raises_after_yield():
        yield
        raise RuntimeError

    with pytest.raises(RuntimeError):
        with loop_scheduler.async_ctx(raises_after_yield()):
            pass


def test_task_timeout():
    loop = asyncio.new_event_loop()
    loop.set_debug(True)

    # First check a normal (sub timeout) situation
    with LoopScheduler(loop=loop, timeout=0.1) as scheduler:
        # Make sure the sleep is bigger than our timeout
        scheduler.await_(asyncio.sleep(0.001))

    # Now one where we time out
    with pytest.raises(concurrent.futures.TimeoutError) as excinfo:
        with LoopScheduler(loop=loop, timeout=0.1) as scheduler:
            scheduler.await_(asyncio.sleep(1.0))
    assert asyncio.sleep.__name__ in str(excinfo.value)

    # Test supplying a custom name
    with pytest.raises(concurrent.futures.TimeoutError) as excinfo:
        with LoopScheduler(loop=loop, timeout=0.1) as scheduler:
            scheduler.await_(asyncio.sleep(1.0), name="sleepin'...zZzZ")
    assert "sleepin'...zZzZ" in str(excinfo.value)


def test_task_cancel(loop_scheduler):  # pylint: disable=redefined-outer-name
    evt = asyncio.Event()

    async def set_env():
        evt.set()

    loop_scheduler.await_submit(set_env()).result()
    assert evt.is_set()

    evt.clear()
    loop_scheduler.await_submit(set_env()).cancel()
    assert not evt.is_set()


def test_await_futures(loop_scheduler):  # pylint: disable=redefined-outer-name
    """Test that a series of Futures works correctly"""

    async def inception():
        fut = asyncio.Future()
        fut2 = asyncio.Future()
        fut3 = asyncio.Future()

        fut.set_result(True)
        fut2.set_result(fut)
        fut3.set_result(fut2)

        return fut3

    assert loop_scheduler.await_(inception()).result().result().result() is True


def test_await_ctx_futures(loop_scheduler):  # pylint: disable=redefined-outer-name
    """Test that an async context yielding a future is correctly handled i.e. the asyncio future
    should be converted to a concurrent one and the result be propagated back to the asyncio future
    in the context"""

    @contextlib.asynccontextmanager
    async def ctx():
        fut = asyncio.Future()
        try:
            yield fut
        finally:
            assert fut.result() is True

    with loop_scheduler.async_ctx(ctx()) as future:
        assert isinstance(future, concurrent.futures.Future)
        future.set_result(True)
