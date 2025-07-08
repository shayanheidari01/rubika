from typing import Union
import rubpy

class VotePoll:
    async def vote_poll(
            self: "rubpy.Client",
            poll_id: str,
            selection_index: Union[str, int],
    ) -> rubpy.types.Update:
        """
        Vote on a poll option.

        Args:
            poll_id (str): The ID of the poll.
            selection_index (Union[str, int]): The index of the option to vote for.

        Returns:
            rubpy.types.Update: The update indicating the success of the vote.
        """
        return await self.builder('votePoll',
                                  input={
                                      'poll_id': poll_id,
                                      'selection_index': int(selection_index),
                                  })
