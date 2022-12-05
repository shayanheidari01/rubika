from re import findall

class Message:
    __slots__ = (
        'bot',
        'msg',
    )

    def __init__(self, bot, message):
        self.bot = bot
        self.msg = message

    async def reply(self, text):
        return await self.bot.sendText(
            self.msg.get('object_guid'),
            text,
            reply_to_message_id=self.msg.get('message_id')
            )

    async def show(self):
        return self.msg

    async def of_group(self, groups=None):
        if groups == None:
            return self.msg.get('type') == 'Group'
        else:
            if self.msg.get('type') == 'Group':
                return self.msg.get('object_guid') in groups

    async def of_user(self, users=None):
        if users == None:
            return self.msg.get('type') == 'User'
        else:
            if self.msg.get('type') == 'User':
                return self.msg.get('object_guid') in users

    async def id(self):
        return self.msg.get('message_id')

    async def text(self):
        return self.msg.get('message').get('text')

    async def type(self):
        return self.msg.get('message').get('type')

    async def is_text(self):
        return self.msg.get('message').get('type') == 'Text'

    async def author_type(self):
        return self.msg.get('message').get('author_type')

    async def author_object_guid(self, authors=None):
        if authors == None:
            return self.msg.get('message').get('author_object_guid')
        else:
            return self.msg.get('message').get('author_object_guid') in authors

    async def chat_id(self):
        return self.msg.get('object_guid')

    async def is_forward(self):
        message = self.msg.get('message')
        return 'forwarded_from' in message.keys() and message.get('forwarded_from').get('type_from') == 'Channel'

    async def hasAds(self):
        if self.msg.get('message').get('type') == 'Text':
            string = self.msg.get('message').get('text')
            urls = findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
            if urls != []: return True
            elif '@' in string: return True
            for check in ['.ir', '.com', '.org']:
                if check in string: return True
            else:
                return False