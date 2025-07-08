from typing import Optional, Coroutine
from asyncio import run

import rubpy


class Run:
    def run(self: "rubpy.Client", coroutine: Optional[Coroutine] = None, phone_number: str = None):
        """
        Run the client in either synchronous or asynchronous mode.

        Args:
        - coroutine (Optional[Coroutine]): An optional coroutine to run asynchronously.
        - phone_number (str): The phone number to use for starting the client.

        Returns:
        - If running synchronously, returns the initialized client.
        - If running asynchronously, returns None.
        """
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
