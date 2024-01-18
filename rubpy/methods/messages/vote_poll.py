from typing import Union


class VotePoll:
    async def vote_poll(
            self,
            poll_id: str,
            selection_index: Union[str, int],
    ):
        return await self.builder('votePoll',
                                  input={
                                      'poll_id': poll_id,
                                      'selection_index': int(selection_index),
                                  })