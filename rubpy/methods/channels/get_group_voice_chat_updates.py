from time import time


class GetGroupVoiceChatUpdates:
    async def get_group_voice_chat_updates(
            self,
            group_guid: str,
            voice_chat_id: str,
            state: int=None,
    ):
        if state is None:
            state = round(time()) - 150

        return await self.builder('getGroupVoiceChatUpdates',
                                  input={
                                      'group_guid': group_guid,
                                      'voice_chat_id': voice_chat_id,
                                      'state': int(state),
                                  })