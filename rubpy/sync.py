import asyncio
import functools
import inspect
import threading

from rubpy import types
from rubpy.methods import Methods

def async_to_sync(obj, name):
    """
    Wrap an asynchronous function or asynchronous generator method
    to make it synchronous.

    Parameters:
    - obj: Object containing the method.
    - name: Name of the method to wrap.

    Returns:
    Wrapped synchronous function or generator.
    """
    function = getattr(obj, name)
    main_loop = asyncio.get_event_loop()

    def async_to_sync_gen(agen, loop, is_main_thread):
        async def anext(agen):
            try:
                return await agen.__anext__(), False
            except StopAsyncIteration:
                return None, True

        while True:
            if is_main_thread:
                item, done = loop.run_until_complete(anext(agen))
            else:
                item, done = asyncio.run_coroutine_threadsafe(anext(agen), loop).result()

            if done:
                break

            yield item

    @functools.wraps(function)
    def async_to_sync_wrap(*args, **kwargs):
        coroutine = function(*args, **kwargs)

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if threading.current_thread() is threading.main_thread() or not main_loop.is_running():
            if loop.is_running():
                return coroutine
            else:
                if inspect.iscoroutine(coroutine):
                    return loop.run_until_complete(coroutine)

                if inspect.isasyncgen(coroutine):
                    return async_to_sync_gen(coroutine, loop, True)
        else:
            if inspect.iscoroutine(coroutine):
                if loop.is_running():
                    async def coro_wrapper():
                        return await asyncio.wrap_future(asyncio.run_coroutine_threadsafe(coroutine, main_loop))

                    return coro_wrapper()
                else:
                    return asyncio.run_coroutine_threadsafe(coroutine, main_loop).result()

            if inspect.isasyncgen(coroutine):
                if loop.is_running():
                    return coroutine
                else:
                    return async_to_sync_gen(coroutine, main_loop, False)

    setattr(obj, name, async_to_sync_wrap)

def wrap_methods(source):
    """
    Wrap asynchronous methods in a class to make them synchronous.

    Parameters:
    - source: Class containing asynchronous methods.
    """
    for name in dir(source):
        method = getattr(source, name)

        if not name.startswith("_") and (inspect.iscoroutinefunction(method) or inspect.isasyncgenfunction(method)):
            async_to_sync(source, name)

def wrap_types_methods():
    """
    Wrap asynchronous methods in types' classes to make them synchronous.
    """
    for class_name in dir(types):
        cls = getattr(types, class_name)

        if inspect.isclass(cls):
            wrap_methods(cls)

# Wrap all relevant methods in the Client's Methods class
wrap_methods(Methods)

# Wrap types' bound methods
wrap_types_methods()
