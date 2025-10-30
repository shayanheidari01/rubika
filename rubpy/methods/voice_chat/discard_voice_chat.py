import rubpy


class DiscardChatVoiceChat:
    async def discard_coice_chat(
        self: "rubpy.Client", object_guid: str, voice_chat_id: str
    ):
        chat_type = "Group" if object_guid.startswith("g0") else "Channel"
        input = {
            f"{chat_type.lower()}_guid": object_guid,
            "voice_chat_id": voice_chat_id,
        }
        return self.builder(f"discard{chat_type}VoiceChat", input=input)
