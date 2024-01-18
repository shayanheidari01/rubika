import rubpy
from typing import Union, Optional


class GetPollOptionVoters:
    async def get_poll_option_voters(
            self: "rubpy.Client",
            poll_id: str,
            selection_index: Union[str, int],
            start_id: Optional[str] = None,
    ):
        input = {'poll_id': poll_id,
                 'selection_index': selection_index,
                 'start_id': start_id,
                }

        return await self.builder(name='getPollOptionVoters', input=input)