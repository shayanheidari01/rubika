from typing import Optional, Coroutine
import asyncio

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
            if coroutine is not None:
                await coroutine
            await self.get_updates()
            return self

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(main_runner())

        return loop.create_task(main_runner())
