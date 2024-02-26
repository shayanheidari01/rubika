import rubpy
import time
import asyncio
import pathlib

try:
    import aiortc
    from aiortc.contrib.media import MediaPlayer
except ImportError:
    aiortc = None

class VoiceChatPlayer:
    async def heartbeat(self: "rubpy.Client", chat_guid: str, voice_chat_id: str) -> None:
        """
        Continuously sends heartbeat updates for a voice chat.

        Args:
            chat_guid (str): The GUID of the chat.
            voice_chat_id (str): The ID of the voice chat.
        """
        while True:
            try:
                await self.get_group_voice_chat_updates(chat_guid, voice_chat_id, int(time.time()))
                await asyncio.sleep(10)

            except (rubpy.exceptions.InvalidAuth, rubpy.exceptions.InvalidInput):
                break

            except Exception:
                continue

    async def speaking(self: "rubpy.Client", chat_guid: str, voice_chat_id: str) -> None:
        """
        Sends voice chat activity updates.

        Args:
            chat_guid (str): The GUID of the chat.
            voice_chat_id (str): The ID of the voice chat.
        """
        while True:
            try:
                await self.send_group_voice_chat_activity(chat_guid, voice_chat_id)
                await asyncio.sleep(1)

            except (rubpy.exceptions.InvalidAuth, rubpy.exceptions.InvalidInput):
                break

            except Exception:
                continue

    async def voice_chat_player(self: "rubpy.Client", chat_guid: str, media: "pathlib.Path", loop: bool = False) -> bool:
        """
        Initiates a voice chat player for a given chat and media file.

        Args:
            chat_guid (str): The GUID of the chat.
            media (pathlib.Path): The path to the media file.
            loop (bool, optional): Whether to loop the media. Defaults to False.

        Returns:
            bool: True if the voice chat player is initiated successfully, False otherwise.
        """
        if aiortc is None:
            return False

        class AudioFileTrack(aiortc.MediaStreamTrack):
            kind: str = 'audio'

            def __init__(self, player):
                super().__init__() 
                self.player = player

            async def recv(self):
                frame = await self.player.audio.recv()
                return frame

        chat_info = await self.get_info(chat_guid)
        voice_chat_id = chat_info.chat.find_keys('{}_voice_chat_id'.format('group' if chat_guid.startswith('g0') else 'channel'))

        if voice_chat_id is None:
            voice_chat = (await self.create_group_voice_chat(chat_guid) if chat_guid.startswith('g0') else
                          await self.create_channel_voice_chat(chat_guid))
            voice_chat_id = voice_chat.find_keys('voice_chat_id')
            if voice_chat_id is None:
                voice_chat_id = (voice_chat.group_voice_chat_update.voice_chat_id if chat_guid.startswith('g0') else
                                voice_chat.channel_voice_chat_update.voice_chat_id)

        self.logger.info(f'Voice chat created and started on chat guid: {chat_guid} and voice id: {voice_chat_id}...')

        pc = aiortc.RTCPeerConnection()
        track = AudioFileTrack(MediaPlayer(media, media.split('.')[-1], loop=loop, decode=True))
        pc.addTrack(track)

        sdp_offer_local = await pc.createOffer()
        await pc.setLocalDescription(sdp_offer_local)

        connect = await self.join_voice_chat(chat_guid, voice_chat_id, sdp_offer_local.sdp)
        sdp_offer = connect.sdp_answer_data

        await self.set_voice_chat_state(chat_guid, voice_chat_id)
        asyncio.create_task(self.speaking(chat_guid, voice_chat_id))
        remote_description = aiortc.RTCSessionDescription(sdp_offer, 'answer')
        asyncio.create_task(self.heartbeat(chat_guid, voice_chat_id))
        await pc.setRemoteDescription(remote_description)

        @pc.on('iceconnectionstatechange')
        def on_iceconnectionstatechange():
            self.logger.info(f'ICE connection state is: {pc.iceConnectionState}')

        @pc.on('connectionstatechange')
        def on_connectionstatechange():
            self.logger.info(f'Connection state is: {pc.connectionState}')

        @pc.on('track')
        def on_track(event):
            self.logger.info(f'Track {event}')

        return True
