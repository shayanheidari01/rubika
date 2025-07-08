import rubpy

class SendGroupVoiceChatActivity:
    async def send_group_voice_chat_activity(
            self: "rubpy.Client",
            chat_guid: str,
            voice_chat_id: str,
            participant_object_guid: str = None,
            activity: str = 'Speaking',
    ) -> rubpy.types.Update:
        """
        Set group voice chat activity.

        Args:
        - chat_guid (str): The GUID of the Chat.
        - voice_chat_id (str): The voice chat ID.
        - participant_object_guid (str): Participant object guid, Defualt is `self.guid`.
        - activity (str): Literal['Speaking'] and Defualt is `Speaking`.

        Returns:
        - rubpy.types.Update: Update object confirming the change in default access.
        """
        input = {
            'chat_guid': chat_guid,
            'voice_chat_id': voice_chat_id,
            'activity': activity,
            'participant_object_guid': participant_object_guid or self.guid,
        }
        return await self.builder(name='sendGroupVoiceChatActivity', input=input)