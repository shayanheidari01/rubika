import rubpy
from typing import Literal

class SetVoiceChatState:
    async def set_voice_chat_state(
            self: "rubpy.Client",
            chat_guid: str,
            voice_chat_id: str,
            participant_object_guid: str = None,
            action: Literal['Mute', 'Unmute'] = 'Unmute',
    ) -> rubpy.types.Update:
        """
        Set group or channel voice chat state.

        Args:
        - chat_guid (str): The GUID of the Chat.
        - voice_chat_id (str): The voice chat ID.
        - participant_object_guid (str): Participant object guid, Defualt is `self.guid`.
        - action (str): Literal['Mute', 'Unmute'] and Defualt is `Unmute`.

        Returns:
        - rubpy.types.Update: Update object confirming the change in default access.
        """
        input = dict(
            chat_guid=chat_guid,
            voice_chat_id=voice_chat_id,
            action=action,
            participant_object_guid=participant_object_guid or self.guid,
        )
        name = 'setGroupVoiceChatState' if chat_guid.startswith('g0') else 'setChannelVoiceChatState'
        return await self.builder(name=name, input=input)