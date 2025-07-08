import rubpy
from rubpy.types import Update

class GetPrivacySetting:
    """
    Provides a method to get the current user's privacy setting.

    Methods:
    - get_privacy_setting: Get the current user's privacy setting.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_privacy_setting(
            self: "rubpy.Client"
    ) -> Update:
        """
        Get the current user's privacy setting.

        Returns:
        - rubpy.types.Update: The current user's privacy setting.
        """
        return await self.builder('getPrivacySetting')  # type: ignore
