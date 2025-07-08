from time import time
from typing import Optional, Union
import rubpy

class GetContactsUpdates:
    async def get_contacts_updates(
            self: "rubpy.Client",
            state: Optional[Union[str, int]] = round(time()) - 150,
    ) -> rubpy.types.Update:
        """
        Get updates related to contacts.

        Args:
            self (rubpy.Client): The rubpy client.
            state (Optional[Union[str, int]], optional):
                The state parameter to filter updates. Defaults to `round(time()) - 150`.

        Returns:
            rubpy.types.Update: The update related to contacts.
        """
        return await self.builder(name='getContactsUpdates',
                                  input={'state': int(state)})
