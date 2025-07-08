import rubpy

class UpdateUsername:
    """
    Provides a method to update the username of the user.

    Methods:
    - update_username: Update the username of the user.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def update_username(
            self: "rubpy.Client",
            username: str
    ) -> rubpy.types.Update:
        """
        Update the username of the user.

        Parameters:
        - username (str): The new username for the user.

        Returns:
        - rubpy.types.Update: The updated user information after the username update.
        """
        return await self.builder('updateUsername', input={'username': username.replace('@', '')})
