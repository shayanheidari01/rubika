from .connections import Connections

__all__ = ('Methods')

class Methods:
    __slots__ = (
        'token',
        'connections',
    )

    def __init__(self, token, session):
        self.token = token
        self.connections = Connections(
            session=session,
            token=token,
        )

    # Messages
    async def sendMessage(
        self,
        chat_id,
        text,
        chat_keypad = None,
        disable_notification = False,
        inline_keypad = None,
        reply_to_message_id = None,
        chat_keypad_type = None,
    ):
        data = {
            'text': text,
            'chat_id': chat_id,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
        }
        if chat_keypad:
            data['chat_keypad'] = chat_keypad.dict()
            data['chat_keypad_type'] = chat_keypad_type
        if inline_keypad:
            data['inline_keypad'] = inline_keypad.dict()
        response = self.connections.post(
            method='sendMessage',
            body=data,
        )
        return await response

    async def getMe(self):
        response = await self.connections.post(
            method='getMe',
            body={},
        )
        return response.get('bot')