import rubpy

class JoinVoiceChat:
    async def join_voice_chat(
            self: "rubpy.Client",
            chat_guid: str,
            voice_chat_id: str,
            sdp_offer_data: str,
    ):
        """
        Join to the group | channel voice chat.

        Args:
        - chat_guid (str): The GUID of the Chat.
        - voice_chat_id (str): The voice chat ID.
        - sdp_offer_data (str): SDP offer data.

        Returns:
        - rubpy.types.Update: Update object confirming the change in default access.
        """
        input = dict(
            chat_guid=chat_guid,
            voice_chat_id=voice_chat_id,
            sdp_offer_data=sdp_offer_data,
            self_object_guid=self.guid,
        )
        return await self.builder(name='joinGroupVoiceChat' if chat_guid.startswith('g0') else 'joinChannelVoiceChat',
                                  input=input)