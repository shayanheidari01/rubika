from .methods import MethodsMaker
from .connections import WebSocket
from .handler import Message
from ..util import Utils
from random import randint
from time import time
from asyncio import run as RUN


__all__ = ['_Client']


class _Client:
    __slots__ = (
        '__make__',
        'websocket',
        'utils',
        '__auth',
    )
    def __init__(self, auth):
        self.__make__ = MethodsMaker(auth=auth,)
        self.__auth = auth
        self.websocket = WebSocket(auth,).updatesHandler
        self.utils = Utils()
        del auth

    # Messages
    async def __sendMessage(
        self,
        object_guid,
        text,
        reply_to_message_id=None,
    ):
        data = {
            'object_guid': object_guid,
            'rnd': f'{randint(10000000, 999999999)}',
            'text': text.strip(),
            'reply_to_message_id': reply_to_message_id
        }
        metadata = self.utils.textParser(text)
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
            data['text'] = metadata[1].strip()

        data = await self.__make__.request(
            method='sendMessage',
            data=data,
        )
        return data

    async def sendText(self, object_guid, text, reply_to_message_id=None,):
        return await self.__sendMessage(
            object_guid=object_guid,
            text=text,
            reply_to_message_id=reply_to_message_id,
            )

    async def editMessage(self, object_guid, new_text, message_id):
        data = {
            'object_guid': object_guid,
            'text': new_text.strip(),
            'message_id': message_id,
        }
        metadata = self.utils.textParser(new_text)
        if metadata[0] != []:
            data['metadata'] = {'meta_data_parts': metadata[0]}
            data['text'] = metadata[1].strip()
        return await self.__make__.request(
            method='editMessage',
            data=data,
        )

    async def sendFile(self, object_guid, file, caption=None, reply_to_message_id=None):
        if '/' in file:
            file_name = file.split('/')[-1]
        else:
            file_name = file.split('\\')[-1] if '\\' in file else file

        return await self._baseSendFiles(
            file_type = 'file',
            file_bytes = open(file, 'rb').read(),
            file_name = file_name,
            object_guid = object_guid,
            text = caption,
            reply_to_message_id = reply_to_message_id,
        )

    async def sendPhoto(self, object_guid, file, caption=None, reply_to_message_id=None):
        if '/' in file:
            file_name = file.split('/')[-1]
        else:
            file_name = file.split('\\')[-1] if '\\' in file else file

        return await self._baseSendFiles(
            file_type = 'image',
            file_bytes = open(file, 'rb').read(),
            file_name = file_name,
            object_guid = object_guid,
            text = caption,
            reply_to_message_id = reply_to_message_id,
        )

    async def sendVoice(self, object_guid, voice, caption=None, reply_to_message_id=None):
        if '/' in voice:
            file_name = voice.split('/')[-1]
        else:
            file_name = voice.split('\\')[-1] if '\\' in voice else voice

        return await self._baseSendFiles(
            file_type = 'voice',
            file_bytes = open(voice, 'rb').read(),
            file_name = file_name,
            object_guid = object_guid,
            text = caption,
            reply_to_message_id = reply_to_message_id,
        )

    async def sendMusic(self, object_guid, music, caption=None, reply_to_message_id=None):
        if '/' in music:
            file_name = music.split('/')[-1]
        else:
            file_name = music.split('\\')[-1] if '\\' in music else music

        return await self._baseSendFiles(
            file_type = 'music',
            file_bytes = open(music, 'rb').read(),
            file_name = file_name,
            object_guid = object_guid,
            text = caption,
            reply_to_message_id = reply_to_message_id,
            path = music,
        )

    async def sendGif(self, object_guid, gif, caption=None, reply_to_message_id=None):
        if '/' in gif:
            file_name = gif.split('/')[-1]
        else:
            file_name = gif.split('\\')[-1] if '\\' in gif else gif

        return await self._baseSendFiles(
            file_type = 'gif',
            file_bytes = open(gif, 'rb').read(),
            file_name = file_name,
            object_guid = object_guid,
            text = caption,
            reply_to_message_id = reply_to_message_id,
            path = gif,
        )

    async def sendVideo(self, object_guid, video, caption=None, reply_to_message_id=None):
        if '/' in video:
            file_name = video.split('/')[-1]
        else:
            file_name = video.split('\\')[-1] if '\\' in video else video

        return await self._baseSendFiles(
            file_type = 'video',
            file_bytes = open(video, 'rb').read(),
            file_name = file_name,
            object_guid = object_guid,
            text = caption,
            reply_to_message_id = reply_to_message_id,
            path = video,
        )

    async def deleteMessages(self, object_guid, message_ids_list, delete_type='Global'):
        data = {
            'object_guid': object_guid,
            'message_ids': message_ids_list,
            'type': delete_type
        }
        return await self.__make__.request(
            method='deleteMessages',
            data=data,
        )

    async def forwardMessages(self, from_object_guid, message_ids, to_object_guid):
        data = {
			'from_object_guid': from_object_guid,
			'message_ids': message_ids,
			'rnd': f'{randint(100000,999999999)}',
			'to_object_guid': to_object_guid
		}
        return await self.__make__.request(
            method='forwardMessages',
            data=data,
        )

    async def createPoll(self, object_guid, question='این نظر سنجی توسط rubpy ارسال شده است و برای تست است',
        allows_multiple_answers=False, is_anonymous=True, reply_to_message_id=0,
        type='Regular', options=['rubpy', 'rubpy'], correct_option_index=None, explanation=None):
            if type == 'Regular':
                data = {
                    "allows_multiple_answers": allows_multiple_answers,
                    "is_anonymous": is_anonymous,
                    "object_guid": object_guid,
                    "options": options,
                    "question": question,
                    "reply_to_message_id": int(reply_to_message_id),
                    "rnd": randint(100000000, 999999999),
                    "type": type
                }
            else:
                data = {
                    "allows_multiple_answers": allows_multiple_answers,
                    "correct_option_index": correct_option_index,
                    "is_anonymous": is_anonymous,
                    "object_guid": object_guid,
                    "options": options,
                    "question": question,
                    "reply_to_message_id": reply_to_message_id,
                    "rnd": randint(100000000, 999999999),
                    "type": "Quiz"
                }
                if explanation != None:
                    data['explanation'] = explanation
            return await self.__make__.request(
            method='createPoll',
            data=data,
        )

    async def votePoll(self, poll_id, selection_index):
        data = {
            'poll_id': poll_id,
            'selection_index': selection_index
        }
        return await self.__make__.request(
            method='votePoll',
            data=data,
        )
    
    async def getPollStatus(self, poll_id):
        return await self.__make__.request(
            method='getPollStatus',
            data={'poll_id': poll_id},
        )

    async def getPollOptionVoters(self, poll_id, selection_index, start_id=None):
        data = {
            'poll_id': poll_id,
            'selection_index': selection_index,
            'start_id': start_id
        }
        return await self.__make__.request(
            method='getPollOptionVoters',
            data=data,
        )

    async def setPinMessage(self, object_guid, message_id, action='Pin'):
        data = {
            'action': action,
            'message_id': message_id,
            'object_guid': object_guid
        }
        return await self.__make__.request(
            method='setPinMessage',
            data=data,
        )

    async def getMessagesByID(self, object_guid, message_ids):
        data = {'object_guid': object_guid, 'message_ids': message_ids}
        return await self.__make__.request(
            method='getMessagesByID',
            data=data,
        )

    async def getMessagesInterval(self, object_guid, middle_message_id):
        data = {'object_guid': object_guid, 'middle_message_id': middle_message_id}
        return await self.__make__.request(
            method='getMessagesInterval',
            data=data,
        )

    async def getMessagesUpdates(self, object_guid):
        data = {'object_guid': object_guid, 'state': str(round(time()) - 200)}
        data = await self.__make__.request(
            method='getMessagesUpdates',
            data=data,
        )
        return data.get('updated_messages')

    async def seenChannelMessages(self, channel_guid, min_id, max_id):
        data = {"channel_guid": channel_guid, "max_id": int(max_id), "min_id": int(min_id)}
        return await self.__make__.request(
            method='seenChannelMessages',
            data=data,
        )

    # Users
    async def getUserInfo(self, user_guid):
        return await self.__make__.request(
            method='getUserInfo',
            data={'user_guid': user_guid},
        )

    async def updateUsername(self, username):
        if '@' in username: username.replace('@', '')
        data = {
			'username': username,
			'updated_parameters': ['username']
		}
        return await self.__make__.request(
            method='updateUsername',
            data=data,
        )

    async def updateProfile(self, **kwargs):
        data = {
			'first_name': kwargs.get('first_name'),
			'last_name': kwargs.get('last_name'),
			'bio': kwargs.get('bio'),
			'updated_parameters': list(kwargs.keys())
		}
        return await self.__make__.request(
            method='updateProfile',
            data=data,
        )

    async def setBlockUser(self, user_guid, action='Block'):
        data = {'action': action,'user_guid': user_guid}
        return await self.__make__.request(
            method='setBlockUser',
            data=data,
        )

    async def deleteUserChat(self, user_guid, last_deleted_message_id):
        data = {'last_deleted_message_id': last_deleted_message_id, 'user_guid': user_guid}
        return await self.__make__.request(
            method='deleteUserChat',
            data=data,
        )

    async def getObjectByUsername(self, username):
        if '@' in username: username.replace('@', '')
        return await self.__make__.request(
            method='getObjectByUsername',
            data={'username': username},
        )

    # Chats
    async def getChats(self, start_id=None):
        response = await self.__make__.request(
            method='getChats',
            data={'start_id': start_id},
        )
        return response.get('chats')

    async def seenChats(self, seen_list):
        '''
            The message ID must be of integer type
            An Example:
                {"object_guid": 341386188755760}
        '''
        return await self.__make__.request(
            method='seenChats',
            data={'seen_list': seen_list},
        )

    async def sendChatActivity(self, object_guid, action):
        data = {'activity': action, 'object_guid': object_guid}
        return await self.__make__.request(
            method='sendChatActivity',
            data=data,
        )

    async def getChatsUpdates(self):
        response = await self.__make__.request(
            method='getChatsUpdates',
            data={'state': str(round(time()) - 250)},
        )
        return response.get('chats')

    async def deleteChatHistory(self, object_guid, last_message_id):
        data = {'object_guid': object_guid, 'last_message_id': last_message_id}
        return await self.__make__.request(
            method='deleteChatHistory',
            data=data,
        )

    async def setActionChat(self, object_guid):
        data = {'action': 'Mute', 'object_guid': object_guid}
        return await self.__make__.request(
            method='setActionChat',
            data=data,
        )

    # Groups
    async def banGroupMember(self, group_guid, member_guid, action='Set'):
        data = {'group_guid': group_guid, 'member_guid': member_guid, 'action': action}
        return await self.__make__.request(
            method='banGroupMember',
            data=data,
        )

    async def addGroupMembers(self, group_guid, member_guids):
        data = {'group_guid': group_guid, 'member_guids': member_guids}
        return await self.__make__.request(
            method='banGroupMember',
            data=data,
        )

    async def getGroupAdminMembers(self, group_guid, get_admin_guids=False):
        in_chat_members = await self.__make__.request('getGroupAdminMembers', {'group_guid': group_guid})
        in_chat_members = in_chat_members.get('in_chat_members')
        admin_list_guids = []
        if get_admin_guids:
            for guid in in_chat_members:
                admin_list_guids.append(guid.get('member_guid'))
            return admin_list_guids
        else:
            return in_chat_members

    async def setGroupDefaultAccess(self, group_guid, access_list):
        data = {'access_list': access_list, 'group_guid': group_guid}
        return await self.__make__.request(
            method='setGroupDefaultAccess',
            data=data,
        )

    async def getGroupAllMembers(self, group_guid, start_id=None):
        data = {'group_guid': group_guid, 'start_id': start_id}
        return await self.__make__.request(
            method='getGroupAllMembers',
            data=data,
        )

    async def getGroupInfo(self, group_guid):
        return await self.__make__.request('getGroupInfo', {'group_guid': group_guid})

    async def getGroupLink(self, group_guid):
        result = await self.__make__.request('getGroupLink', {'group_guid': group_guid}, 5)
        return result.get('join_link')

    async def setGroupLink(self, group_guid):
        return await self.__make__.request('setGroupLink', {'group_guid': group_guid})

    async def getBannedGroupMembers(self, group_guid):
        return await self.__make__.request('getBannedGroupMembers', {'group_guid': group_guid})

    async def setGroupTimer(self, group_guid, time):
        data = {'group_guid': group_guid, 'slow_mode': time, 'updated_parameters': ['slow_mode']}
        return await self.__make__.request('editGroupInfo', data, 4)

    async def setGroupAdmin(self, group_guid, member_guid, access_list, action='SetAdmin'):
        data = {'group_guid': group_guid, 'access_list': access_list, 'action': action, 'member_guid': member_guid}
        if action == 'UnsetAdmin':
            data = {'group_guid': group_guid, 'action': action, 'member_guid': member_guid}
        return await self.__make__.request('setGroupAdmin', data, custum_client=True)

    async def joinGroup(self, group_link):
        return await self.__make__.request('joinGroup', {'hash_link': group_link.split('/')[-1]},)

    async def groupPreviewByJoinLink(self, group_link):
        return await self.__make__.request('groupPreviewByJoinLink', {'hash_link': group_link.split('/')[-1]},)

    async def leaveGroup(self, group_guid):
        return await self.__make__.request('leaveGroup', {'group_guid': group_guid},)

    async def getGroupMentionList(self, group_guid):
        return await self.__make__.request('getGroupMentionList', {'group_guid': group_guid},)

    async def addGroup(self, group_title, member_guids):
        data = {'title': group_title, 'member_guids': member_guids}
        return await self.__make__.request('addGroup', data,)

    async def getGroupOnlineCount(self, group_guid):
        data = await self.__make__.request('getGroupOnlineCount', {'group_guid': group_guid})
        return data.get('online_count')

    # Channels
    async def addChannelMembers(self, channel_guid, member_guids):
        data = {'channel_guid': channel_guid, 'member_guids': member_guids}
        return await self.__make__.request('addChannelMembers', data,)

    async def getChannelAllMembers(self, channel_guid, search_text=None, start_id=None):
        data = {'channel_guid': channel_guid, 'search_text': search_text, 'start_id': start_id}
        return await self.__make__.request('getChannelAllMembers', data,)

    async def getChannelInfo(self, channel_guid):
        return await self.__make__.request('getChannelInfo', {'channel_guid': channel_guid}, 5)

    async def getChannelLink(self, channel_guid):
        return await self.__make__.request('getChannelLink', {'channel_guid': channel_guid}, 5)

    async def setChannelLink(self, channel_guid):
        return await self.__make__.request('setChannelLink', {'channel_guid': channel_guid})

    async def channelPreviewByJoinLink(self, channel_link):
        return await self.__make__.request('channelPreviewByJoinLink', {'hash_link': channel_link.split('/')[-1]})

    async def joinChannelByLink(self, channel_link):
        return await self.__make__.request('joinChannelByLink', {'hash_link': channel_link.split('/')[-1]})

    async def joinChannelAction(self, channel_guid, action='Join'):
        data = {'action': action, 'channel_guid': channel_guid}
        return await self.__make__.request('joinChannelAction', data,)

    async def addChannel(self, channel_title, channel_type='Public', member_guids=None):
        data = {'channel_type': channel_type, 'title': channel_title, 'member_guids': member_guids or []}
        return await self.__make__.request('addChannel', data, 5)

    async def removeChannel(self, channel_guid):
        return await self.__make__.request('removeChannel', {'channel_guid': channel_guid})

    # contacts
    async def addAddressBook(self, phone, first_name, last_name=None):
        data = {'first_name': first_name, 'last_name': last_name, 'phone': phone}
        return await self.__make__.request('addAddressBook', data)

    async def getContacts(self):
        return await self.__make__.request('getContacts', {})

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
        data = dict(
            exclude_object_guids=exclude_object_guids,
            include_object_guids=include_object_guids,
            exclude_chat_types=exclude_chat_types,
            include_chat_types=include_chat_types,
            folder_id=folder_id, is_add_to_top=is_add_to_top,
            name=name,
        )
        return await self.__make__.request('addFolder', data,)

    async def changePassword(self, new_hint, new_password, old_password):
        data = {'new_hint': new_hint, 'new_password': new_password, 'password': old_password}
        return await self.__make__.request('changePassword', data)

    async def requestChangePhoneNumber(self, new_phone_numer):
        if new_phone_numer.startswith('0'):
            phone_number = f'98{new_phone_numer[:1]}'
        elif new_phone_numer.startswith('+98'):
            phone_number = f'98{new_phone_numer[:1]}'
        data = {'new_phone_number': phone_number}
        return await self.__make__.request('requestChangePhoneNumber', data, 4)

    async def turnOffTwoStep(self, password):
        return await self.__make__.request('turnOffTwoStep', {'password': password})

    async def getMySessions(self):
        return await self.__make__.request('getMySessions', {})

    # stickers
    async def getMyStickerSets(self):
        return await self.__make__.request('getMyStickerSets', {},)

    # Bots
    async def getBotInfo(self, bot_guid):
        return await self.__make__.request('getBotInfo', {'bot_guid': bot_guid},)

    # Files
    async def requestSendFile(self, file_name, mime, size):
        data = {'file_name': file_name, 'mime': mime, 'size': size}
        return await self.__make__.request('requestSendFile', data)

    # extras
    async def searchGlobalObjects(self, search_text):
        data = await self.__make__.request('searchGlobalObjects', {'search_text': search_text})
        return data.get('objects')

    async def getLinkFromAppUrl(self, app_url):
        return await self.__make__.request('getLinkFromAppUrl', {'app_url': app_url})

    async def uploadAvatar(self, object_guid, image, thumbnail_file_id=None):
        data = {'object_guid': object_guid, 'thumbnail_file_id': None, 'main_file_id': None}
        with open(image, 'rb') as file:
            my_image = file.read()
            file.close(); del file
        rsf = await self.requestSendFile(f'image{randint(1, 999)}.jpg', 'jpg', str(len(my_image)))
        await self.__make__.__uploader__(
            upload_url = rsf.get('upload_url'),
            access_hash_send = rsf.get('access_hash_send'),
            file_id = rsf.get('id'),
            file_bytes = my_image,
        )
        data['thumbnail_file_id'] = thumbnail_file_id or rsf.get('id')
        data['main_file_id'] = rsf.get('id')
        return await self.__make__.request('uploadAvatar', data)

    async def _baseSendFiles(self, file_type, file_bytes, **kwargs):
        data = {
            'file_inline': {
                'dc_id': None,
                'file_id': None,
                'type':'File',
                'file_name': kwargs.get('file_name'),
                'size': None,
                'mime': None,
                'access_hash_rec': None
            },
            'object_guid': kwargs.get('object_guid'),
            'text': kwargs.get('text'),
            'rnd': f'{randint(100000,999999999)}',
            'reply_to_message_id': kwargs.get('reply_to_message_id'),
        }

        file_type, mime = file_type.lower(), kwargs.get('file_name').split('.')[-1]
        size = str(len(file_bytes))
        rsf = await self.requestSendFile(
            file_name = kwargs.get('file_name') if not file_type == 'voice' else f'rubpy{randint(100, 1000)}.ogg',
            mime = mime,
            size = size
            )
        access_hash_rec = await self.__make__.__uploader__(
            upload_url = rsf.get('upload_url'),
            access_hash_send = rsf.get('access_hash_send'),
            file_id = rsf.get('id'),
            file_bytes = file_bytes,
        )

        if file_type == 'file':
            data['file_inline']['mime'] = mime
            data['file_inline']['size'] = size
            data['file_inline']['access_hash_rec'] = access_hash_rec
            data['file_inline']['dc_id'] = rsf.get('dc_id')
            data['file_inline']['file_id'] = rsf.get('id')

        elif file_type == 'image':
            data['file_inline']['mime'] = mime
            data['file_inline']['size'] = size
            data['file_inline']['type'] = 'Image'
            data['file_inline']['access_hash_rec'] = access_hash_rec
            data['file_inline']['dc_id'] = rsf.get('dc_id')
            data['file_inline']['file_id'] = rsf.get('id')
            data['file_inline']['thumb_inline'] = self.utils.getThumbnail(file_bytes).decode('utf-8')
            width, height = self.utils.getImageSize(file_bytes)
            data['file_inline']['width'] = width
            data['file_inline']['height'] = height

        elif file_type == 'voice':
            data['file_inline']['file_name'] = f'rubpy{randint(100, 1000)}.ogg'
            data['file_inline']['mime'] = 'ogg'
            data['file_inline']['type'] = 'Voice'
            data['file_inline']['size'] = size
            data['file_inline']['time'] = await self.utils.get_voice_duration(file_bytes)
            data['file_inline']['access_hash_rec'] = access_hash_rec
            data['file_inline']['dc_id'] = rsf.get('dc_id')
            data['file_inline']['file_id'] = rsf.get('id')

        elif file_type == 'music':
            data['file_inline']['mime'] = mime
            data['file_inline']['type'] = 'Music'
            data['file_inline']['size'] = size
            data['file_inline']['time'] = await self.utils.get_voice_duration(file_bytes)
            data['file_inline']['access_hash_rec'] = access_hash_rec
            data['file_inline']['dc_id'] = rsf.get('dc_id')
            data['file_inline']['file_id'] = rsf.get('id')
            data['file_inline']['auto_play'] = False
            data['file_inline']['height'] = 0.0
            data['file_inline']['width'] = 0.0
            data['file_inline']['music_performer'] = await self.utils.getMusicArtist(kwargs.get('path'))

        elif file_type == 'gif':
            data['file_inline']['mime'] = mime
            data['file_inline']['type'] = 'Gif'
            data['file_inline']['size'] = size
            data['file_inline']['time'] = await self.utils.getVideoDuration(kwargs.get('path'))
            data['file_inline']['access_hash_rec'] = access_hash_rec
            data['file_inline']['dc_id'] = rsf.get('dc_id')
            data['file_inline']['file_id'] = rsf.get('id')
            data['file_inline']['auto_play'] = False
            data['file_inline']['height'] = 300
            data['file_inline']['width'] = 600
            data['file_inline']['thumb_inline'] = await self.utils.thumb_inline()

        elif file_type == 'video':
            data['file_inline']['mime'] = mime
            data['file_inline']['type'] = 'Video'
            data['file_inline']['size'] = size
            data['file_inline']['time'] = await self.utils.getVideoDuration(kwargs.get('path'))
            data['file_inline']['access_hash_rec'] = access_hash_rec
            data['file_inline']['dc_id'] = rsf.get('dc_id')
            data['file_inline']['file_id'] = rsf.get('id')
            data['file_inline']['auto_play'] = False
            data['file_inline']['height'] = 300
            data['file_inline']['width'] = 600
            data['file_inline']['thumb_inline'] = await self.utils.thumb_inline()

        return await self.__make__.request(
            method = 'sendMessage',
            data = data,
        )

    async def download(self, object_guid=None, message_id=None, from_link=None, save=False, file_name=None, **kwargs):
        file_id = kwargs.get('file_id')

        if file_id != None:
            size = kwargs.get('size')
            dc_id = kwargs.get('dc_id')
            access_hash_rec = kwargs.get('access_hash_rec')

        elif from_link != None and from_link.startswith('http'):
            geted_data = await self.getLinkFromAppUrl(from_link)
            geted_data = geted_data.get('link').get('open_chat_data')
            geted_data = await self.getMessagesByID(geted_data.get('object_guid'), [geted_data.get('message_id')])
            message_data = geted_data.get('messages')[0].get('file_inline')
            file_id = message_data.get('file_id')
            size = message_data.get('size')
            dc_id = message_data.get('dc_id')
            access_hash_rec = message_data.get('access_hash_rec')
            file_name = message_data.get('file_name')

        elif object_guid and message_id != None:
            geted_data = await self.getMessagesByID(object_guid, [message_id])
            message_data = geted_data.get('messages')[0].get('file_inline')
            file_id = message_data.get('file_id')
            size = message_data.get('size')
            dc_id = message_data.get('dc_id')
            access_hash_rec = message_data.get('access_hash_rec')
            file_name = message_data.get('file_name')

        url = 'https://messenger{}.iranlms.ir/GetFile.ashx'.format(dc_id)
        headers = {
            'auth': self.__auth,
            'file-id': file_id,
			'access-hash-rec': access_hash_rec
        }
        start_index = 0

        while True:
            if start_index <= 131072:
                headers['start-index'], headers['last-index'] = '0', str(size)
                response = await self.__make__.cns.GET(url, headers=headers)
                file += response.data
                if save:
                    with open(file_name, 'wb+') as my_file:
                        my_file.write(file)
                        my_file.close()
                        return True
                else: return file
            else:
                for i in range(0, size, 131072):
                    headers['start-index'], headers['last-index'] = str(i), str(i + 131072 if i + 131072 <= size else size)
                    response = await self.__make__.cns.GET(url, headers=headers)
                    file += response.data
                    continue

    # Updates
    def newUpdatesHandler(self, func):
        async def runner():
            async for i in self.websocket():
                await func(Message(self, i))
        RUN(runner())

    def Handler(self, func):
        async def runner():
            print('This method will be removed in the update version 5.1.0 and later, please use newUpdatesHandler')
            async for i in self.websocket():
                await func(Message(self, i))
        RUN(runner())

    def run(self, func):
        RUN(func())