import rubpy
from rubpy.types import Update

class GetTwoPasscodeStatus:
    """
    Provides a method to get the two-passcode status for the user.

    Methods:
    - get_two_passcode_status: Get the two-passcode status for the user.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_two_passcode_status(
            self: "rubpy.Client"
    ) -> Update:
        """
        Get the two-passcode status for the user.

        Returns:
        - rubpy.types.Update: The two-passcode status for the user.
        """
        return await self.builder('getTwoPasscodeStatus')  # type: ignore
