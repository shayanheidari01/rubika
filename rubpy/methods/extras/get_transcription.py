import rubpy
from typing import Union

class GetTranscription:
    async def get_transcription(
            self: "rubpy.Client",
            message_id: Union[str, int],
            transcription_id: str,
    ) -> rubpy.types.Update:
        """
        Get transcription for a specific message.

        Args:
            message_id (Union[str, int]): The ID of the message.
            transcription_id (str): The ID of the transcription.

        Returns:
            rubpy.types.Update: The update containing the requested transcription.
        """
        data = dict(
            message_id=int(message_id),
            transcription_id=transcription_id,
        )

        return await self.builder(name='getTranscription', input=data)
