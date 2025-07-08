import rubpy
from time import time

class GetGroupVoiceChatUpdates:
    async def get_group_voice_chat_updates(
            self: "rubpy.Client",
            group_guid: str,
            voice_chat_id: str,
            state: int=None,
    ) -> rubpy.types.Update:
        """
        Get voice chat updates for a group.

        Args:
        - group_guid (str): The GUID of the group.
        - voice_chat_id (str): The ID of the voice chat.
        - state (int, optional): The state for updates. If not provided, it defaults to the current time.

        Returns:
        - rubpy.types.Update: Update object containing the group voice chat updates.
        """
        if state is None:
            state = round(time()) - 150

        return await self.builder('getGroupVoiceChatUpdates',
                                  input={
                                      'group_guid': group_guid,
                                      'voice_chat_id': voice_chat_id,
                                      'state': int(state),
                                  })
