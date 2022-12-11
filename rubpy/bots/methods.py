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

    async def sendPoll(
        self,
        chat_id,
        question,
        options,
        chat_keypad = None,
        disable_notification = False,
        inline_keypad = None,
        reply_to_message_id = None,
        chat_keypad_type = None,
    ):
        data = {
            'chat_id': chat_id,
            'options': options,
            'question': question,
            'chat_keypad': chat_keypad,
            'inline_keypad': inline_keypad,
            'chat_keypad_type': chat_keypad_type,
            'reply_to_message_id': reply_to_message_id,
            'disable_notification': disable_notification,
        }
        response = self.connections.post(
            method='sendPoll',
            body=data,
        )
        return await response

    async def sendLocation(
        self,
        chat_id,
        latitude,
        longitude,
        chat_keypad = None,
        disable_notification = False,
        inline_keypad = None,
        reply_to_message_id = None,
        chat_keypad_type = None,
    ):
        data = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'chat_keypad': chat_keypad,
            'disable_notification': disable_notification,
            'inline_keypad': inline_keypad,
            'reply_to_message_id': reply_to_message_id,
            'chat_keypad_type': chat_keypad_type,
        }
        response = self.connections.post(
            method='sendLocation',
            body=data,
        )
        return await response

    async def sendSticker(
        self,
        chat_id,
        sticker_id,
        chat_keypad = None,
        disable_notification = False,
        inline_keypad = None,
        reply_to_message_id = None,
        chat_keypad_type = None,
    ):
        data = {
            'chat_id': chat_id,
            'sticker_id': sticker_id,
            'chat_keypad': chat_keypad,
            'disable_notification': disable_notification,
            'inline_keypad': inline_keypad,
            'reply_to_message_id': reply_to_message_id,
            'chat_keypad_type': chat_keypad_type,
        }
        response = self.connections.post(
            method='sendSticker',
            body=data,
        )
        return await response

    async def sendContact(
        self,
        chat_id,
        first_name,
        last_name,
        phone_number,
        chat_keypad = None,
        disable_notification = False,
        inline_keypad = None,
        reply_to_message_id = None,
        chat_keypad_type = None,
    ):
        data = {
            'chat_id': chat_id,
            'last_name': last_name,
            'first_name': first_name,
            'chat_keypad': chat_keypad,
            'phone_number': phone_number,
            'inline_keypad': inline_keypad,
            'chat_keypad_type': chat_keypad_type,
            'reply_to_message_id': reply_to_message_id,
            'disable_notification': disable_notification,
        }
        response = self.connections.post(
            method='sendContact',
            body=data,
        )
        return await response

    async def forwardMessage(
        self,
        from_chat_id,
        message_id,
        to_chat_id,
        disable_notification = False,
    ):
        data = {
            'from_chat_id': from_chat_id,
            'message_id': message_id,
            'to_chat_id': to_chat_id,
            'disable_notification': disable_notification,
        }
        response = self.connections.post(
            method='forwardMessage',
            body=data,
        )
        return await response

    async def editMessageText(
        self,
        chat_id,
        message_id,
        text,
    ):
        data = {
            'text': text,
            'chat_id': chat_id,
            'message_id': message_id,
        }
        response = self.connections.post(
            method='editMessageText',
            body=data,
        )
        return await response

    async def editMessageKeypad(
        self,
        chat_id,
        message_id,
        inline_keypad,
    ):
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_keypad': inline_keypad.dict(),
        }
        response = self.connections.post(
            method='editMessageKeypad',
            body=data,
        )
        return await response

    async def editChatKeypad(
        self,
        chat_id,
        chat_keypad,
    ):
        data = {
            'chat_id': chat_id,
            'chat_keypad_type': 'New',
            'chat_keypad': chat_keypad.dict(),
        }
        response = self.connections.post(
            method='editChatKeypad',
            body=data,
        )
        return await response

    async def removeChatKeypad(
        self,
        chat_id,
    ):
        data = {
            'chat_id': chat_id,
            'chat_keypad_type': 'Remove',
        }
        response = self.connections.post(
            method='editChatKeypad',
            body=data,
        )
        return await response

    async def deleteMessage(
        self,
        chat_id,
        message_id,
    ):
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
        }
        response = self.connections.post(
            method='deleteMessage',
            body=data,
        )
        return await response

    async def sendFile(
        self,
        chat_id,
        file_id,
        chat_keypad = None,
        disable_notification = False,
        inline_keypad = None,
        reply_to_message_id = None,
        chat_keypad_type = None,
    ):
        data = {
            'chat_id': chat_id,
            'file_id': file_id,
            'chat_keypad': chat_keypad,
            'disable_notification': disable_notification,
            'inline_keypad': inline_keypad,
            'reply_to_message_id': reply_to_message_id,
            'chat_keypad_type': chat_keypad_type,
        }
        response = self.connections.post(
            method='sendFile',
            body=data,
        )
        return await response

    async def requestSendFile(
        self,
        file_type
    ):
        response = self.connections.post(
            method='requestSendFile',
            body = {'type': file_type},
        )
        return await response

    async def getFile(
        self,
        file_id,
    ):
        response = self.connections.post(
            method='getFile',
            body = {'file_id': file_id},
        )
        return await response

    async def setCommands(
        self,
        bot_commands,
    ):
        data = {
            'bot_commands': [
                command.dict() for command in bot_commands
            ]
        }
        response = self.connections.post(
            method='setCommands',
            body = data,
        )
        return await response

    async def updateBotEndpoints(
        self,
        url,
        type,
    ):
        data = {
            'url': url,
            'type': type,
        }
        response = self.connections.post(
            method='updateBotEndpoints',
            body = data,
        )
        return await response

    async def getMe(self):
        response = await self.connections.post(
            method='getMe',
            body={},
        )
        return response.get('bot')
    
    async def getChat(
        self,
        chat_id,
    ):
        response = self.connections.post(
            method='getChat',
            body={'chat_id': chat_id},
        )
        return await response
    
    async def getUpdates(
        self,
        limit = 10,
        offset_id = None,
    ):
        data = {
            'limit': limit,
        }
        if offset_id: data['offset_id'] = offset_id
        response = self.connections.post(
            method='getUpdates',
            body=data,
        )
        return await response