from .methods import Methods
from .connections import WebSocket
from aiohttp import ClientSession
from asyncio import run as RUN
from .handler import Message

__all__ = ('_Client')

class _Client:
    __slots__ = (
        'auth',
        'account_guid',
        'methods',
        'account_info',
    )

    def __init__(self, auth, account_guid=None):
        self.account_guid = account_guid
        self.auth = auth
        self.account_info = None
        self.methods = None

    async def sendText(self, object_guid, text, reply_to_message_id=None, mention=None):
        response = self.methods.sendText(object_guid, text, reply_to_message_id, mention)
        return await response

    async def editMessage(self, object_guid, new_text, message_id):
        response = self.methods.editMessage(object_guid, new_text, message_id)
        return await response

    async def sendFile(self, object_guid, file, caption=None, reply_to_message_id=None):
        response = self.methods.sendFile(object_guid, file, caption, reply_to_message_id)
        return await response

    async def sendPhoto(self, object_guid, file, caption=None, reply_to_message_id=None):
        response = self.methods.sendPhoto(object_guid, file, caption, reply_to_message_id)
        return await response

    async def sendVoice(self, object_guid, voice, caption=None, reply_to_message_id=None):
        response = self.methods.sendVoice(object_guid, voice, caption, reply_to_message_id)
        return await response

    async def sendMusic(self, object_guid, music, caption=None, reply_to_message_id=None):
        response = self.methods.sendMusic(object_guid, music, caption, reply_to_message_id)
        return await response

    async def sendGif(self, object_guid, gif, caption=None, reply_to_message_id=None):
        response = self.methods.sendGif(object_guid, gif, caption, reply_to_message_id)
        return await response

    async def sendVideo(self, object_guid, video, caption=None, reply_to_message_id=None):
        response = self.methods.sendGif(object_guid, video, caption, reply_to_message_id)
        return await response

    async def deleteMessages(self, object_guid, message_ids_list, delete_type='Global'):
        response = self.methods.deleteMessages(object_guid, message_ids_list, delete_type)
        return await response

    async def forwardMessages(self, from_object_guid, message_ids, to_object_guid):
        response = self.methods.forwardMessages(from_object_guid, message_ids, to_object_guid)
        return await response

    async def createPoll(self, object_guid, question='این نظر سنجی توسط rubpy ارسال شده است و برای تست است',
        allows_multiple_answers=False, is_anonymous=True, reply_to_message_id=0,
        type='Regular', options=['rubpy', 'rubpy'], correct_option_index=None, explanation=None):
            response = self.methods.createPoll(object_guid, question,
            allows_multiple_answers, is_anonymous, reply_to_message_id,
            type, options, correct_option_index, explanation)
            return await response

    async def votePoll(self, poll_id, selection_index):
        response = self.methods.votePoll(poll_id, selection_index)
        return await response

    async def getPollStatus(self, poll_id):
        response = self.methods.getPollStatus(poll_id)
        return await response

    async def getPollOptionVoters(self, poll_id, selection_index, start_id=None):
        response = self.methods.getPollOptionVoters(poll_id, selection_index, start_id)
        return await response

    async def setPinMessage(self, object_guid, message_id, action='Pin'):
        response = self.methods.setPinMessage(object_guid, message_id, action)
        return await response

    async def getMessagesByID(self, object_guid, message_ids):
        response = self.methods.getMessagesByID(object_guid, message_ids)
        return await response

    async def getMessagesInterval(self, object_guid, middle_message_id):
        response = self.methods.getMessagesInterval(object_guid, middle_message_id)
        return await response

    async def getMessagesUpdates(self, object_guid):
        response = self.methods.getMessagesUpdates(object_guid)
        return await response

    async def seenChannelMessages(self, channel_guid, min_id, max_id):
        response = self.methods.seenChannelMessages(channel_guid, min_id, max_id)
        return await response

    # Users
    async def getUserInfo(self, user_guid):
        response = self.methods.getUserInfo(user_guid)
        return await response

    async def updateUsername(self, username):
        response = self.methods.updateUsername(username)
        return await response

    async def updateProfile(self, **kwargs):
        response = self.methods.updateProfile(kwargs)
        return await response

    async def setBlockUser(self, user_guid, action='Block'):
        response = self.methods.setBlockUser(user_guid, action)
        return await response

    async def deleteUserChat(self, user_guid, last_deleted_message_id):
        response = self.methods.deleteUserChat(user_guid, last_deleted_message_id)
        return await response

    async def getObjectByUsername(self, username):
        response = self.methods.getObjectByUsername(username)
        return await response

    # Chats
    async def getChats(self, start_id=None):
        response = self.methods.getChats(start_id)
        return await response

    async def seenChats(self, seen_list):
        '''
            The message ID must be of integer type
            An Example:
                {"object_guid": 341386188755760}
        '''
        response = self.methods.seenChats(seen_list)
        return await response

    async def sendChatActivity(self, object_guid, action):
        response = self.methods.sendChatActivity(object_guid, action)
        return await response

    async def getChatsUpdates(self):
        response = self.methods.getChatsUpdates()
        return await response

    async def deleteChatHistory(self, object_guid, last_message_id):
        response = self.methods.deleteChatHistory(object_guid, last_message_id)
        return await response

    async def setActionChat(self, object_guid):
        response = self.methods.setActionChat(object_guid)
        return await response

    # Groups
    async def banGroupMember(self, group_guid, member_guid, action='Set'):
        response = self.methods.banGroupMember(group_guid, member_guid, action)
        return await response

    async def addGroupMembers(self, group_guid, member_guids):
        response = self.methods.addGroupMembers(group_guid, member_guids)
        return await response

    async def getGroupAdminMembers(self, group_guid, get_admin_guids=False):
        response = self.methods.getGroupAdminMembers(
            group_guid, get_admin_guids)
        return await response

    async def setGroupDefaultAccess(self, group_guid, access_list):
        response = self.methods.setGroupDefaultAccess(
            group_guid, access_list)
        return await response

    async def getGroupAllMembers(self, group_guid, start_id=None):
        response = self.methods.getGroupAllMembers(
            group_guid, start_id)
        return await response

    async def getGroupInfo(self, group_guid):
        response = self.methods.getGroupInfo(
            group_guid)
        return await response

    async def getGroupLink(self, group_guid):
        response = self.methods.getGroupLink(
            group_guid)
        return await response

    async def setGroupLink(self, group_guid):
        response = self.methods.setGroupLink(
            group_guid)
        return await response

    async def getBannedGroupMembers(self, group_guid):
        response = self.methods.getBannedGroupMembers(
            group_guid)
        return await response

    async def setGroupTimer(self, group_guid, time):
        response = self.methods.setGroupTimer(
            group_guid, time)
        return await response

    async def setGroupAdmin(self, group_guid, member_guid, access_list, action='SetAdmin'):
        response = self.methods.setGroupAdmin(
            group_guid, member_guid, access_list, action)
        return await response

    async def joinGroup(self, group_link):
        response = self.methods.joinGroup(
            group_link)
        return await response

    async def groupPreviewByJoinLink(self, group_link):
        response = self.methods.groupPreviewByJoinLink(
            group_link)
        return await response

    async def leaveGroup(self, group_guid):
        response = self.methods.leaveGroup(
            group_guid)
        return await response

    async def getGroupMentionList(self, group_guid):
        response = self.methods.getGroupMentionList(
            group_guid)
        return await response

    async def addGroup(self, group_title, member_guids):
        response = self.methods.addGroup(
            group_title, member_guids)
        return await response

    async def getGroupOnlineCount(self, group_guid):
        response = self.methods.getGroupOnlineCount(
            group_guid)
        return await response

    # Channels
    async def addChannelMembers(self, channel_guid, member_guids):
        response = self.methods.addChannelMembers(
            channel_guid, member_guids)
        return await response

    async def getChannelAllMembers(self, channel_guid, search_text=None, start_id=None):
        response = self.methods.getChannelAllMembers(
            channel_guid, search_text, start_id)
        return await response

    async def getChannelInfo(self, channel_guid):
        response = self.methods.getChannelInfo(
            channel_guid)
        return await response

    async def getChannelLink(self, channel_guid):
        response = self.methods.getChannelLink(
            channel_guid)
        return await response

    async def setChannelLink(self, channel_guid):
        response = self.methods.setChannelLink(
            channel_guid)
        return await response

    async def channelPreviewByJoinLink(self, channel_link):
        response = self.methods.channelPreviewByJoinLink(
            channel_link)
        return await response

    async def joinChannelByLink(self, channel_link):
        response = self.methods.joinChannelByLink(
            channel_link)
        return await response

    async def joinChannelAction(self, channel_guid, action='Join'):
        response = self.methods.joinChannelAction(
            channel_guid, action)
        return await response

    async def addChannel(self, channel_title, channel_type='Public', member_guids=None):
        response = self.methods.addChannel(
            channel_title, channel_type, member_guids)
        return await response

    async def removeChannel(self, channel_guid):
        response = self.methods.addChannel(
            channel_guid)
        return await response

    # contacts
    async def addAddressBook(self, phone, first_name, last_name=None):
        response = self.methods.addAddressBook(
            phone, first_name, last_name)
        return await response

    async def getContacts(self):
        response = self.methods.getContacts()
        return await response

    async def deleteContact(self):
        pass

    # settings
    async def addFolder(
        self,
        name,
        exclude_chat_types=[],
        exclude_object_guids=[],
        include_chat_types=[],
        include_object_guids=[],
        is_add_to_top=True,
        folder_id=''
    ):
        response = self.methods.addFolder(
            name,
            exclude_chat_types,
            exclude_object_guids,
            include_chat_types,
            include_object_guids,
            is_add_to_top,
            folder_id,
        )
        return await response

    async def changePassword(self, new_hint, new_password, old_password):
        response = self.methods.changePassword(
            new_hint, new_password, old_password
        )
        return await response

    async def requestChangePhoneNumber(self, new_phone_numer):
        response = self.methods.requestChangePhoneNumber(
            new_phone_numer
        )
        return await response

    async def turnOffTwoStep(self, password):
        response = self.methods.turnOffTwoStep(password)
        return await response

    async def getMySessions(self):
        response = self.methods.getMySessions()
        return await response

    # stickers
    async def getMyStickerSets(self):
        response = self.methods.getMyStickerSets()
        return await response

    # Bots
    async def getBotInfo(self, bot_guid):
        response = self.methods.getBotInfo(bot_guid)
        return await response

    # Files
    async def requestSendFile(self, file_name, mime, size):
        response = self.methods.requestSendFile(file_name, mime, size)
        return await response

    # extras
    async def searchGlobalObjects(self, search_text):
        response = self.methods.searchGlobalObjects(search_text)
        return await response

    async def getLinkFromAppUrl(self, app_url):
        response = self.methods.getLinkFromAppUrl(app_url)
        return await response

    async def uploadAvatar(self, object_guid, image, thumbnail_file_id=None):
        response = self.methods.uploadAvatar(object_guid, image, thumbnail_file_id)
        return await response

    async def _baseSendFiles(self, file_type, file_bytes, **kwargs):
        response = self.methods._baseSendFiles(file_type, file_bytes, kwargs)
        return await response

    async def download(self, object_guid, message_id, save=False):
        response = self.methods.download(object_guid, message_id, save)
        return await response

    def handler(self, func):
        async def runner():
            async with ClientSession() as session:
                methods = Methods(self.auth, session=session, account_guid=self.account_guid)
                self.methods = methods
                if self.account_guid != None:
                    account_info = await methods.getUserInfo(self.account_guid)
                    self.account_info = account_info.get('user')
                ws = WebSocket(self.auth, session=session)
                async for update in ws.updatesHandler():
                    await func(methods, Message(methods, message=update))
        RUN(runner())

    def run(self, func):
        async def runner():
            async with ClientSession() as session:
                methods = Methods(self.auth, session=session, account_guid=self.account_guid)
                if self.account_guid != None:
                    account_info = await methods.getUserInfo(self.account_guid)
                    self.account_info = account_info.get('user')
                    self.methods = methods
                await func(methods)
        RUN(runner())

    def MessageUpdates(self, func):
        async def runner():
            async with ClientSession() as session:
                methods = Methods(self.auth, session=session, account_guid=self.account_guid)
                self.methods = methods
                if self.account_guid != None:
                    account_info = await methods.getUserInfo(self.account_guid)
                    self.account_info = account_info.get('user')
                ws = WebSocket(self.auth, session=session)
                async for update in ws.updatesHandler():
                    await func(methods, Message(methods, message=update))
        RUN(runner())

    def ChatUpdates(self, func):
        async def runner():
            async with ClientSession() as session:
                methods = Methods(self.auth, session=session, account_guid=self.account_guid)
                self.methods = methods
                if self.account_guid != None:
                    account_info = await methods.getUserInfo(self.account_guid)
                    self.account_info = account_info.get('user')
                ws = WebSocket(self.auth, session=session)
                async for update in ws.updatesHandler(
                    chat_updates=True, message_updates=False
                ):
                    await func(update)
        RUN(runner())