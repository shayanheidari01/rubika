from .methods import Methods
from .connections import WebSocket
from aiohttp import ClientSession
from asyncio import run as RUN
from .handler import Message

__all__ = ('_Client')

class _Client:
    __slots__ = ('auth')

    def __init__(self, auth):
        self.auth = auth

    def handler(self, func):
        async def runner():
            async with ClientSession() as session:
                async with Methods(self.auth, session=session) as methods:
                    async with WebSocket(self.auth, session=session) as ws:
                        async for update in ws.updatesHandler():
                            await func(methods, Message(methods, message=update))
        RUN(runner())

    def run(self, func):
        async def runner():
            async with ClientSession() as session:
                async with Methods(self.auth, session=session) as methods:
                    await func(methods)
        RUN(runner())