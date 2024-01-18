from typing import Optional, Coroutine
from asyncio import run

import rubpy


class Run:
    def run(self: "rubpy.Client", coroutine: Optional[Coroutine] = None, phone_number: str = None):
        async def main_runner():
            await self.start(phone_number=phone_number)
            await self.connection.get_updates()

        if coroutine:
            run(coroutine)

        run(main_runner())