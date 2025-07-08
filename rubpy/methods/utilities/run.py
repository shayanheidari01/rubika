from typing import Optional, Coroutine
from asyncio import run
import threading

import rubpy


class Run:
    def run(self: "rubpy.Client", coroutine: Optional[Coroutine] = None, phone_number: str = None):
        # print(self.is_sync)
        if self.is_sync:
            self.start(phone_number=phone_number)
            self.get_updates()
            return self

        async def main_runner():
            await self.start(phone_number=phone_number)
            await self.get_updates()

        if coroutine:
            run(coroutine)

        run(main_runner())