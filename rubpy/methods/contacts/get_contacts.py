import rubpy
from typing import Optional, Union


class GetContacts:
    async def get_contacts(
            self: "rubpy.Client",
            start_id: Optional[Union[str, int]] = None,
    ):
        return self.builder(name='getContacts',
                            input={'start_id': str(start_id)})