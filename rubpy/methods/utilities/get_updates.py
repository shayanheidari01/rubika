import rubpy

class GetUpdates:
    async def get_updates(self: "rubpy.Client") -> "rubpy.types.Update":
        """
        Get updates from the server.

        Returns:
        - rubpy.types.Update: An Update object containing information about the updates.
        """

        while True:
            try:
                return await self.connection.get_updates()

            except Exception:
                pass