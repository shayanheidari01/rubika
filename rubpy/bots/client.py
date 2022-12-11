from .methods import Methods
from asyncio import run as RUN
from asyncio import create_task
from aiohttp import ClientSession
from json import dump

__all__ = (
    '_Client',
)

class _Client:
    __slots__ = (
        'token',
    )

    def __init__(self, token):
        self.token = token

    async def handler(self):
        pass

    def run(self, func):
        async def runner():
            async with ClientSession() as session:
                self.session = session
                methods = Methods(self.token, session=session)
                with open('setup.json', 'w+') as setup:
                    me = await methods.getMe()
                    me = {'bot': me}
                    dump(me, setup, indent=4, sort_keys=True)
                    setup.close()
                del setup
                task = create_task(func(methods))
                await task
        RUN(runner())