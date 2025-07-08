import rubpy
from typing import Optional, Union

class GetContacts:
    async def get_contacts(
            self: "rubpy.Client",
            start_id: Optional[Union[str, int]] = None,
    ) -> rubpy.types.Update:
        """
        Get a list of contacts.

        Args:
            self ("rubpy.Client"): The rubpy client.
            start_id (Optional[Union[str, int]], optional): Start ID for pagination. Defaults to None.

        Returns:
            rubpy.types.Update: The result of the API call.
        """
        return self.builder(name='getContacts', input={'start_id': str(start_id)})
