import asyncio
import concurrent.futures

from async_generator import async_generator, yield_, asynccontextmanager
import pytest

from pytray.aiothreads import LoopScheduler


@pytest.fixture
def loop_scheduler():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    with LoopScheduler(loop=loop) as scheduler:
        yield scheduler


async def simple(arg):
    await asyncio.sleep(0.1)
    return arg


def test_simple_await_submit(loop_scheduler):
    future = loop_scheduler.await_submit(simple('Done!'))
    assert future.result() == 'Done!'


def test_simple_await(loop_scheduler):
    result = loop_scheduler.await_(simple('Done!'))
    assert result == 'Done!'


def test_async_context(loop_scheduler):
    sequence = []

    @asynccontextmanager
    @async_generator
    async def do():
        sequence.append('Entered')
        await yield_(10)
        sequence.append('Exiting')

    with loop_scheduler.async_ctx(do()) as value:
        assert value == 10

    assert sequence == ['Entered', 'Exiting']


def test_async_context_exception(loop_scheduler):
    sequence = []

    @asynccontextmanager
    @async_generator
    async def raises_before_yield():
        raise RuntimeError
        await yield_()

    with pytest.raises(RuntimeError):
        with loop_scheduler.async_ctx(raises_before_yield()):
            pass

    @asynccontextmanager
    @async_generator
    async def raises_after_yield():
        await yield_()
        raise RuntimeError

    with pytest.raises(RuntimeError):
        with loop_scheduler.async_ctx(raises_after_yield()):
            pass


def test_task_timeout():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    # First check a normal (sub timeout) situation
    with LoopScheduler(loop=loop, timeout=0.1) as scheduler:
        # Make sure the sleep is bigger than our timeout
        scheduler.await_(asyncio.sleep(0.001))

    # Now one where we time out
    with pytest.raises(concurrent.futures.TimeoutError):
        with LoopScheduler(loop=loop, timeout=0.1) as scheduler:
            scheduler.await_(asyncio.sleep(1.))
