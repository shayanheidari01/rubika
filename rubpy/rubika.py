from .connections.requests import Requests
from random import randint
from .connections.websocket import WebSocket
from time import time as time_stamp
from .tools import Tools
from urllib3 import PoolManager
import asyncio
from mutagen.mp3 import MP3
from io import BytesIO
try: from tinytag import TinyTag
except ModuleNotFoundError: TinyTag = None

class Client(object):
    def __init__(self, auth):
        self.__requests = Requests(auth)
        self.send = self.__requests.send
        self.upload = self.__requests.uploadFile
        self.websocket = WebSocket(auth).handler
        self._auth = auth
        self.tools = Tools()
        self.__pool_manager = PoolManager()
        self.run = asyncio.run

    async def sendMessage(self, object_guid, text, reply_to_message_id=None, meta_data=None):
        data = {'object_guid': object_guid, 'rnd': f'{randint(100000, 999999999)}', 'text': text, 'reply_to_message_id': reply_to_message_id}
        if meta_data != None: data['metadata'] = {'meta_data_parts': meta_data}
        meta_data = self.tools.analyzeString(text)
        if meta_data.get('metadata') != []:
            data['metadata'] = {'meta_data_parts': meta_data.get('metadata')}
            data['text'] = meta_data.get('string')
        return await self.send('sendMessage', data)

    async def sendPhoto(self, object_guid, image, caption=None, reply_to_message_id=None):
        file_name = f'shayan-heidari{randint(1, 999)}.jpg'
        data = {'file_inline': {'dc_id': None, 'file_id': None, 'type':'Image',
                'file_name': file_name, 'size': None, 'mime': 'jpg', 'access_hash_rec': None,
                'width': None, 'height': None, 'thumb_inline': None
            },
            'object_guid': object_guid, 'text': caption, 'rnd': f'{randint(100000,999999999)}', 'reply_to_message_id': reply_to_message_id
        }
        if image.startswith('http'):
            response = self.__pool_manager.request('GET', image)
            content_length = dict(response.headers).get('Content-Length')
            if content_length == None:
                content_length = dict(response.headers).get('content-length')
            file_bytes = response.data
            requestSendFile = await self.requestSendFile(file_name, 'jpg', content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file_bytes)
            width, height = self.tools.getImageSize(file_bytes)
            data['file_inline']['thumb_inline'] = self.tools.getThumbnail(file_bytes).decode('utf-8')
            data['file_inline']['size'] = content_length
            data['file_inline']['width'] = width
            data['file_inline']['height'] = height
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')
        else:
            with open(image, 'rb') as my_file:
                file = my_file.read()
                my_file.close()
            content_length = str(len(file))
            requestSendFile = await self.requestSendFile(file_name, 'jpg', content_length)
            width, height = self.tools.getImageSize(file)
            data['file_inline']['thumb_inline'] = self.tools.getThumbnail(file).decode('utf-8')
            data['file_inline']['size'] = content_length
            data['file_inline']['width'] = width
            data['file_inline']['height'] = height
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file)
            data['file_inline']['file_id'] = requestSendFile.get('id')

        return await self.send('sendMessage', data, 5)

    async def sendFile(self, object_guid, file, caption=None, reply_to_message_id=None):
        mime = f".{file.split('.')[-1]}"
        file_name = f'shayan-heidari{randint(1, 999)}{mime}'
        data = {
            'file_inline': {
                'dc_id': None,
                'file_id': None,
                'type':'File',
                'file_name': file_name,
                'size': None,
                'mime': mime,
                'access_hash_rec': None
            },
            'object_guid': object_guid,
            'text': caption,
            'rnd': f'{randint(100000,999999999)}',
            'reply_to_message_id': reply_to_message_id
        }
        if file.startswith('http'):
            response = self.__pool_manager.request('GET', file)
            content_length = dict(response.headers).get('Content-Length')
            if content_length == None:
                content_length = dict(response.headers).get('content-length')
            file_bytes = response.data
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file_bytes)
            data['file_inline']['size'] = content_length
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')
        else:
            with open(file, 'rb') as my_file:
                file = my_file.read()
                my_file.close()
            content_length = str(len(file))
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file)
            data['file_inline']['size'] = content_length
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')

        return await self.send('sendMessage', data, 5)

    async def sendVoice(self, object_guid, voice, caption=None, reply_to_message_id=None):
        mime = '.ogg'
        file_name = f'shayan-heidari{randint(1, 999)}{mime}'
        data = {
            'file_inline': {
                'dc_id': None,
                'file_id': None,
                'type':'Voice',
                'file_name': file_name,
                'size': None,
                'time': None,
                'mime': mime,
                'access_hash_rec': None
            },
            'object_guid': object_guid,
            'text': caption,
            'rnd': f'{randint(100000,999999999)}',
            'reply_to_message_id': reply_to_message_id
        }
        if voice.startswith('http'):
            response = self.__pool_manager.request('GET', voice)
            content_length = dict(response.headers).get('Content-Length')
            if content_length == None:
                content_length = dict(response.headers).get('content-length')
            file_bytes = response.data
            duration = await self.get_voice_duration(file_bytes)
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file_bytes)
            data['file_inline']['size'] = content_length
            data['file_inline']['time'] = duration
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')
        else:
            with open(voice, 'rb') as my_file:
                file = my_file.read()
                my_file.close()
            duration = await self.get_voice_duration(file)
            content_length = str(len(file))
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file)
            data['file_inline']['size'] = content_length
            data['file_inline']['time'] = duration
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')

        return await self.send('sendMessage', data, 5)

    async def sendMusic(self, object_guid, music, music_performer = None, file_name = None, caption=None, reply_to_message_id=None):
        mime = f".{music.split('.')[-1]}"
        file_name = f'{file_name}{mime}'
        data = {
            'file_inline': {
                'dc_id': None,
                'file_id': None,
                'auto_play': False,
                'height': 0.0,
                'width': 0.0,
                'music_performer': music_performer,
                'type':'Music',
                'file_name': file_name,
                'size': None,
                'time': None,
                'mime': mime,
                'access_hash_rec': None
            },
            'object_guid': object_guid,
            'text': caption,
            'rnd': f'{randint(100000,999999999)}',
            'reply_to_message_id': reply_to_message_id
        }
        if music.startswith('http'):
            response = self.__pool_manager.request('GET', music)
            content_length = dict(response.headers).get('Content-Length')
            if content_length == None:
                content_length = dict(response.headers).get('content-length')
            file_bytes = response.data
            duration = await self.get_voice_duration(file_bytes)
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file_bytes)
            data['file_inline']['size'] = content_length
            data['file_inline']['time'] = duration
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')
        else:
            with open(music, 'rb') as my_file:
                file = my_file.read()
                my_file.close()
            duration = await self.get_voice_duration(file)
            content_length = str(len(file))
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file)
            data['file_inline']['size'] = content_length
            data['file_inline']['time'] = duration
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')

        return await self.send('sendMessage', data, 5)

    async def sendGif(self, object_guid, gif, caption=None, reply_to_message_id=None):
        mime = f".{gif.split('.')[-1]}"
        file_name = f'shayan-heidari{randint(1, 999)}{mime}'
        data = {
            'file_inline': {
                'dc_id': None,
                'file_id': None,
                'auto_play': False,
                'height': 300,
                'width': 600,
                'thumb_inline': 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAAL0lEQVR4nO3NQQ0AAAgEIPVz/Rsbw81BATpJXZiTVSwWi8VisVgsFovFYrFY/DRelEIAZd5yXa4AAAAASUVORK5CYII=',
                'type':'Gif',
                'file_name': file_name,
                'size': None,
                'time': None,
                'mime': mime,
                'access_hash_rec': None
            },
            'object_guid': object_guid,
            'text': caption,
            'rnd': f'{randint(100000,999999999)}',
            'reply_to_message_id': reply_to_message_id
        }
        with open(gif, 'rb') as my_file:
            file = my_file.read()
            my_file.close()
        duration = await self.getVideoDuration(gif)
        content_length = str(len(file))
        requestSendFile = await self.requestSendFile(file_name, mime, content_length)
        is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file)
        data['file_inline']['size'] = content_length
        data['file_inline']['time'] = duration
        data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
        data['file_inline']['access_hash_rec'] = is_uploaded
        data['file_inline']['file_id'] = requestSendFile.get('id')

        return await self.send('sendMessage', data, 5)

    async def sendVideo(self, object_guid, video, caption=None, reply_to_message_id=None):
        mime = f".{video.split('.')[-1]}"
        file_name = f'shayan-heidari{randint(1, 999)}{mime}'
        data = {
            'file_inline': {
                'dc_id': None,
                'file_id': None,
                'auto_play': False,
                'height': 300,
                'width': 600,
                'thumb_inline': 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAAL0lEQVR4nO3NQQ0AAAgEIPVz/Rsbw81BATpJXZiTVSwWi8VisVgsFovFYrFY/DRelEIAZd5yXa4AAAAASUVORK5CYII=',
                'type':'Video',
                'file_name': file_name,
                'size': None,
                'time': None,
                'mime': mime,
                'access_hash_rec': None
            },
            'object_guid': object_guid,
            'text': caption,
            'rnd': f'{randint(100000,999999999)}',
            'reply_to_message_id': reply_to_message_id
        }
        with open(video, 'rb') as my_file:
            file = my_file.read()
            my_file.close()
        duration = await self.getVideoDuration(video)
        content_length = str(len(file))
        requestSendFile = await self.requestSendFile(file_name, mime, content_length)
        is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file)
        data['file_inline']['size'] = content_length
        data['file_inline']['time'] = duration
        data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
        data['file_inline']['access_hash_rec'] = is_uploaded
        data['file_inline']['file_id'] = requestSendFile.get('id')

        return await self.send('sendMessage', data, 5)

    def get_voice_duration(self, file_bytes):
        file = BytesIO()
        file.write(file_bytes)
        file.seek(0)
        audio = MP3(file)
        return audio.info.length

    async def getVideoDuration(self, video):
        if TinyTag != None:
            return round(TinyTag.get(video).duration * 1000)
        else:
            raise ImportWarning('Plaese install <TinyTag> and try again')

    async def uploadAvatar(self, object_guid, image, thumbnail_file_id=None):
        data = {'object_guid': object_guid, 'thumbnail_file_id': None, 'main_file_id': None}
        with open(image, 'rb') as file:
            my_image = file.read()
            file.close(); del file
        requestSendFile = await self.requestSendFile(f'image{randint(1, 999)}.jpg', 'jpg', str(len(my_image)))
        is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'))
        data['thumbnail_file_id'] = thumbnail_file_id or requestSendFile.get('id')
        data['main_file_id'] = requestSendFile.get('id')
        return await self.send('uploadAvatar', data, 5)

    async def requestSendFile(self, file_name, mime, size):
        data = {'file_name': file_name, 'mime': mime, 'size': size}
        response = await self.send('requestSendFile', data, 5)
        return response.get('data')

    async def getChats(self, start_id=None):
        return await self.send('getChats', {'start_id': start_id}, 5)

    async def editMessage(self, message_id, object_guid, new_text, meta_data=None):
        data = {'message_id': message_id, 'object_guid': object_guid, 'text': new_text}
        if meta_data != None: data['metadata'] = {'meta_data_parts': meta_data}
        modes = ['**' , '__' , '``']
        for check in modes:
            if check in new_text:
                meta_data = self.tools.analyzeString(new_text)
                data['metadata'] = {'meta_data_parts': meta_data.get('metadata')}
                data['text'] = meta_data.get('string')
            else: continue
        return await self.send('editMessage', data, 5)

    async def deleteMessages(self, object_guid, message_ids_list, delete_type='Global'):
        data = {'object_guid': object_guid, 'message_ids': message_ids_list, 'type': delete_type}
        return await self.send('deleteMessages', data, 5)

    async def getUserInfo(self, user_guid):
        return await self.send('getUserInfo', {'user_guid': user_guid}, 5)

    async def getMessagesInterval(self, object_guid, middle_message_id):
        data: dict = {'object_guid': object_guid, 'middle_message_id': middle_message_id}
        return await self.send('getMessagesInterval', data, 5)

    async def getObjectByUsername(self, username):
        if '@' in username: username.replace('@', '')
        return await self.send('getObjectByUsername', {'username': username}, 5)

    async def banGroupMember(self, group_guid, member_guid, action='Set'):
        data = {'group_guid': group_guid, 'member_guid': member_guid, 'action': action}
        return await self.send('banGroupMember', data, 5)

    async def addGroupMembers(self, group_guid, member_guids):
        data = {'group_guid': group_guid, 'member_guids': member_guids}
        return await self.send('addGroupMembers', data, 5)

    async def addChannelMembers(self, channel_guid, member_guids):
        data = {'channel_guid': channel_guid, 'member_guids': member_guids}
        return await self.send('addChannelMembers', data, 5)

    async def getGroupAdminMembers(self, group_guid, get_admin_guids=False):
        in_chat_members = await self.send('getGroupAdminMembers', {'group_guid': group_guid}, 5)
        in_chat_members = in_chat_members.get('data').get('in_chat_members')
        admin_list_guids = []
        if get_admin_guids:
            for guid in in_chat_members:
                admin_list_guids.append(guid.get('member_guid'))
            return admin_list_guids
        else:
            return in_chat_members

    async def getMessagesByID(self, object_guid, message_ids):
        data = {'object_guid': object_guid, 'message_ids': message_ids}
        return await self.send('getMessagesByID', data, 5)

    async def setGroupDefaultAccess(self, group_guid, access_list):
        data = {'access_list': access_list, 'group_guid': group_guid}
        return await self.send('setGroupDefaultAccess', data)

    async def getGroupAllMembers(self, group_guid, start_id=None):
        data = {'group_guid': group_guid, 'start_id': start_id}
        return await self.send('getGroupAllMembers', data, 5)

    async def getGroupInfo(self, group_guid):
        return await self.send('getGroupInfo', {'group_guid': group_guid}, 5)

    async def getGroupLink(self, group_guid):
        result = await self.send('getGroupLink', {'group_guid': group_guid}, 5)
        link = result.get('data').get('join_link')
        return link

    async def setGroupLink(self, group_guid):
        return await self.send('setGroupLink', {'group_guid': group_guid}, 5)

    async def getBannedGroupMembers(self, group_guid):
        data = await self.send('getBannedGroupMembers', {'group_guid': group_guid})
        return data.get('data')

    async def setGroupTimer(self, group_guid, time):
        data = {'group_guid': group_guid, 'slow_mode': time, 'updated_parameters': ['slow_mode']}
        return await self.send('editGroupInfo', data)

    async def setGroupAdmin(self, group_guid, member_guid, access_list, action='SetAdmin'):
        data = {'group_guid': group_guid, 'access_list': access_list, 'action': action, 'member_guid': member_guid}
        if action == 'UnsetAdmin':
            data = {'group_guid': group_guid, 'action': action, 'member_guid': member_guid}
        return await self.send('setGroupAdmin', data, 5, custum_client=True)

    async def logout(self):
        return await self.send('logout', {}, 5)

    async def forwardMessages(self, from_object_guid, message_ids, to_object_guid):
        data = {
			'from_object_guid': from_object_guid,
			'message_ids': message_ids,
			'rnd': f'{randint(100000,999999999)}',
			'to_object_guid': to_object_guid
		}
        return await self.send('forwardMessages', data, 5)

    async def seenChats(self, seen_list):
        '''
            The message ID must be of integer type
            An Example:
                {"object_guid": 341386188755760}
        '''
        return await self.send('seenChats', {'seen_list': seen_list})

    async def sendChatActivity(self, object_guid, action):
        data = {'activity': action, 'object_guid': object_guid}
        return await self.send('sendChatActivity', data, 5)

    async def setPinMessage(self, object_guid, message_id, action='Pin'):
        data = {'action': action, 'message_id': message_id, 'object_guid': object_guid}
        return await self.send('setPinMessage', data)

    async def joinGroup(self, group_link):
        return await self.send('joinGroup', {'hash_link': group_link.split('/')[-1]}, 5)

    async def groupPreviewByJoinLink(self, group_link):
        return await self.send('groupPreviewByJoinLink', {'hash_link': group_link.split('/')[-1]}, 5)

    async def leaveGroup(self, group_guid):
        return await self.send('leaveGroup', {'group_guid': group_guid}, 5)

    async def getChannelAllMembers(self, channel_guid, search_text, start_id=None):
        data = {'channel_guid': channel_guid, 'search_text': search_text, 'start_id': start_id}
        return await self.send('getChannelAllMembers', data, 5)

    async def getChatsUpdates(self):
        data = await self.send('getChatsUpdates', {'state': str(round(time_stamp()) - 200)}, 5)
        return data.get('data').get('chats')

    async def getMessagesUpdates(self, object_guid):
        data = {'object_guid': object_guid, 'state': str(round(time_stamp()) - 200)}
        data = await self.send('getMessagesUpdates', data, 5)
        return data.get('data').get('updated_messages')

    async def getMyStickerSets(self):
        return await self.send('getMessagesUpdates', {}, 5)

    async def sendGroupVoiceChatActivity(self, group_guid, voice_chat_id, activity = 'Speaking'):
        data = {'activity': activity, 'chat_guid': group_guid, 'voice_chat_id': voice_chat_id}
        return await self.send('sendGroupVoiceChatActivity', data, 5)

    async def createVoiceChat(self, object_guid):
        method = 'createGroupVoiceChat' if object_guid.startwith('g') else 'createChannelVoiceChat'
        data = 'group' if object_guid.startwith('g') else 'channel'
        return await self.send(method, {f'{data}_guid': object_guid}, 5)

    async def editVoiceChat(self, object_guid, voice_chat_id, title):
        method = 'setGroupVoiceChatSetting' if object_guid.startwith('g') else 'setChannelVoiceChatSetting'
        data = 'group' if object_guid.startwith('g') else 'channel'
        data = {f'{data}_guid': object_guid, 'voice_chat_id': voice_chat_id, 'title': title, 'updated_parameters': ['title']}
        return await self.send(method, data, 5)

    async def discardVoiceChat(self, object_guid, voice_chat_id, title):
        method = 'discardGroupVoiceChat' if object_guid.startwith('g') else 'discardChannelVoiceChat'
        data = 'group' if object_guid.startwith('g') else 'channel'
        data = {f'{data}_guid': object_guid, 'voice_chat_id': voice_chat_id}
        return await self.send(method, data, 5)

    async def getAvatars(self, object_guid):
        return await self.send('getAvatars', {'object_guid': object_guid}, 5)

    async def deleteAvatar(self, object_guid, avatar_id):
        data = {'object_guid': object_guid, 'avatar_id': avatar_id}
        return await self.send('deleteAvatar', data, 5)

    async def download(self, object_guid=None, message_id=None, from_link=None, save=False, file_name=None, **kwargs):
        file = b''

        file_id = kwargs.get('file_id')
        if file_id != None:
            size = kwargs.get('size')
            dc_id = kwargs.get('dc_id')
            access_hash_rec = kwargs.get('access_hash_rec')
        elif from_link != None and from_link.startswith('http'):
            geted_data = await self.getLinkFromAppUrl(from_link)
            geted_data = geted_data.get('link').get('open_chat_data')
            geted_data = await self.getMessagesByID(geted_data.get('object_guid'), [geted_data.get('message_id')])
            message_data = geted_data.get('data').get('messages')[0].get('file_inline')
            file_id = message_data.get('file_id')
            size = message_data.get('size')
            dc_id = message_data.get('dc_id')
            access_hash_rec = message_data.get('access_hash_rec')
            file_name = message_data.get('file_name')
        elif object_guid and message_id != None:
            geted_data = await self.getMessagesByID(object_guid, [message_id])
            message_data = geted_data.get('data').get('messages')[0].get('file_inline')
            file_id = message_data.get('file_id')
            size = message_data.get('size')
            dc_id = message_data.get('dc_id')
            access_hash_rec = message_data.get('access_hash_rec')
            file_name = message_data.get('file_name')

        url = 'https://messenger{}.iranlms.ir/GetFile.ashx'.format(dc_id)
        headers = {
            'auth': self._auth,
            'file-id': file_id,
			'access-hash-rec': access_hash_rec
        }
        start_index = 0

        while True:
            if start_index <= 131072:
                headers['start-index'], headers['last-index'] = '0', str(size)
                response = self.__pool_manager.request('GET', url, headers=headers)
                if response.status == 200:
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
                    response = self.__pool_manager.request('GET', url, headers=headers)
                    if response.status == 200:
                        file += response.data
                        continue

    async def seenChannelMessages(self, channel_guid, min_id, max_id):
        return await self.send('getChannelInfo', {"channel_guid": channel_guid, "max_id": int(max_id), "min_id": int(min_id)})

    async def getChannelInfo(self, channel_guid):
        return await self.send('getChannelInfo', {'channel_guid': channel_guid}, 5)

    async def getGroupMentionList(self, group_guid):
        return await self.send('getGroupMentionList', {'group_guid': group_guid}, 5)

    async def getChannelLink(self, channel_guid):
        return await self.send('getChannelLink', {'channel_guid': channel_guid}, 5)
    
    async def setChannelLink(self, channel_guid):
        return await self.send('setChannelLink', {'channel_guid': channel_guid})

    async def channelPreviewByJoinLink(self, channel_link):
        return await self.send('channelPreviewByJoinLink', {'hash_link': channel_link.split('/')[-1]})

    async def joinChannelByLink(self, channel_link):
        return await self.send('channelPreviewByJoinLink', {'hash_link': channel_link.split('/')[-1]})

    async def updateUsername(self, username):
        if '@' in username: username.replace('@', '')
        data = {
			'username': username,
			'updated_parameters': ['username']
		}
        return await self.send('updateUsername', data)

    async def updateProfile(self, **kwargs):
        data = {
			'first_name': kwargs.get('first_name'),
			'last_name': kwargs.get('last_name'),
			'bio': kwargs.get('bio'),
			'updated_parameters': list(kwargs.keys())
		}
        return await self.send('updateProfile', data)

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
            return await self.send('createPoll', data)

    async def votePoll(self, poll_id, selection_index):
        return await self.send('createPoll', {'poll_id': poll_id, 'selection_index': selection_index})

    async def getPollStatus(self, poll_id):
        return await self.send('getPollStatus', {'poll_id': poll_id}, 5)

    async def getPollOptionVoters(self, poll_id, selection_index, start_id=None):
        data = {'poll_id': poll_id, 'selection_index': selection_index, 'start_id': start_id}
        return await self.send('getPollOptionVoters', data)

    async def getLinkFromAppUrl(self, app_url):
        return await self.send('getLinkFromAppUrl', {'app_url': app_url})

    async def joinChannelAction(self, channel_guid, action='Join'):
        data = {'action': action, 'channel_guid': channel_guid}
        return await self.send('joinChannelAction', data, 5)

    async def deleteChatHistory(self, object_guid, last_message_id):
        data = {'object_guid': object_guid, 'last_message_id': last_message_id}
        return await self.send('deleteChatHistory', data)

    async def searchGlobalObjects(self, search_text):
        data = await self.send('searchGlobalObjects', {'search_text': search_text})
        return data.get('objects')

    async def addAddressBook(self, phone, first_name, last_name=None):
        data = {'first_name': first_name, 'last_name': last_name, 'phone': phone}
        return await self.send('addAddressBook', data)

    async def addGroup(self, group_title, member_guids):
        data = {'title': group_title, 'member_guids': member_guids}
        return await self.send('addAddressBook', data, 5)

    async def addChannel(self, channel_title, channel_type='Public', member_guids=None):
        data = {'channel_type': channel_type, 'title': channel_title, 'member_guids': member_guids or []}
        return await self.send('addChannel', data, 5)

    async def removeChannel(self, channel_guid):
        return await self.send('removeChannel', {'channel_guid': channel_guid})

    async def addFolder(self, name, exclude_chat_types=[], exclude_object_guids=[], include_chat_types=[], include_object_guids=[], is_add_to_top=True, folder_id=''):
        data = dict(exclude_object_guids=exclude_object_guids, include_object_guids=include_object_guids, exclude_chat_types=exclude_chat_types, include_chat_types=include_chat_types, folder_id=folder_id, is_add_to_top=is_add_to_top, name=name)
        return await self.send('addFolder', data, 5)

    async def setBlockUser(self, user_guid, action='Block'):
        data = {'action': action,'user_guid': user_guid}
        return await self.send('setBlockUser', data, 5)

    async def changePassword(self, new_hint, new_password, old_password):
        data = {'new_hint': new_hint, 'new_password': new_password, 'password': old_password}
        return await self.send('changePassword', data, 5)

    async def requestChangePhoneNumber(self, new_phone_numer):
        if new_phone_numer.startswith('0'):
            phone_number = f'98{new_phone_numer[:1]}'
        elif new_phone_numer.startswith('+98'):
            phone_number = f'98{new_phone_numer[:1]}'
        data = {'new_phone_number': phone_number}
        return await self.send('requestChangePhoneNumber', data)

    async def turnOffTwoStep(self, password):
        return await self.send('turnOffTwoStep', {'password': password}, 5)

    async def deleteUserChat(self, user_guid, last_deleted_message_id):
        data = {'last_deleted_message_id': last_deleted_message_id, 'user_guid': user_guid}
        return await self.send('deleteUserChat', data)

    async def deleteChatHistory(self, object_guid, last_message_id):
        data = {'object_guid': object_guid, 'last_message_id': last_message_id}
        return await self.send('deleteChatHistory', data, 5)

    async def getGroupOnlineCount(self, group_guid):
        data = await self.send('getGroupOnlineCount', {'group_guid': group_guid})
        return data.get('online_count')

    async def getContacts(self):
        return await self.send('getContacts', {})

    async def getMySessions(self):
        return await self.send('getMySessions', {})

    async def setActionChat(self, object_guid):
        data = {'action': 'Mute', 'object_guid': object_guid}
        return await self.send('setActionChat', data)

    async def reportObject(self, object_guid, reportType=106, description=None):
        data = {'object_guid': object_guid, 'report_description': description, 'report_type': reportType, 'report_type_object': 'Object'}
        return await self.send('reportObject', data)

    async def requestChangeObjectOwner(self, object_guid, new_owner_user_guid):
        data = {'object_guid': object_guid, 'new_owner_user_guid': new_owner_user_guid}
        return await self.send('requestChangeObjectOwner', data)

    async def getBotInfo(self, bot_guid):
        return await self.send('getBotInfo', {'bot_guid': bot_guid}, 5)

    def Handler(self, func):
        async def runner():
            async for i in self.websocket():
                await func(i)
        asyncio.run(runner())