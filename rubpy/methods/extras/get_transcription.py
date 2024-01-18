import rubpy
from typing import Union


class GetTranscription:
    async def get_transcription(
            self: "rubpy.Client",
            message_id: Union[str, int],
            transcription_id: str,
    ):
        data = dict(
            message_id=int(message_id),
            transcription_id=transcription_id,
        )

        return await self.builder(
            name='getTranscription',
            input=data,
        )