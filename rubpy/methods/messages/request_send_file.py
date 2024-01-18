from typing import Union


class RequestSendFile:
    async def request_send_file(
            self,
            file_name: str,
            size: Union[str, int, float],
            mime: str=None,
    ):
        input = {
            'file_name': file_name,
            'size': int(size),
            'mime': file_name.split('.')[-1] if mime is None else mime
        }
        return await self.builder('requestSendFile',
                                  input=input)