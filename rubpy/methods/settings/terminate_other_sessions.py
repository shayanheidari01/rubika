import rubpy

class TerminateOtherSessions:
    async def terminate_other_sessions(
            self: "rubpy.Client",
    ) -> rubpy.types.Update:
        """
        Terminate other account sessions.

        Returns:
        - rubpy.types.Update: The updated user information after terminating the session.
        """
        return await self.builder('terminateOtherSessions')