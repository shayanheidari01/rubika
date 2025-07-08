import rubpy
import time
import asyncio
import pathlib
import logging

try:
    import aiortc
    from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
    from aiortc.contrib.media import MediaPlayer
except ImportError:
    aiortc = None


class VoiceChatConnection:
    def __init__(self, peer_connection: "RTCPeerConnection", media_player, audio_track, chat_guid, voice_chat_id, client):
        self.pc = peer_connection
        self.player = media_player
        self.track = audio_track
        self.chat_guid = chat_guid
        self.voice_chat_id = voice_chat_id
        self.client = client

    def stop(self):
        if self.player:
            self.player.audio.stop()
        if self.pc:
            asyncio.create_task(self.pc.close())
        if hasattr(self, '_speaking_task'):
            self._speaking_task.cancel()
        if hasattr(self, '_heartbeat_task'):
            self._heartbeat_task.cancel()

    def pause(self):
        self.track.pause()

    def resume(self):
        self.track.resume()

    def replace_track(self, new_media_path: str, loop: bool = False):
        new_player = MediaPlayer(str(new_media_path), decode=True)
        new_track = new_player.audio

        # پیدا کردن اولین sender با kind='audio'
        sender = next((s for s in self.pc.getSenders() if s.track and s.track.kind == "audio"), None)

        if sender:
            sender.replaceTrack(new_track)
            self.track = new_track
            self.player = new_player
        else:
            raise RuntimeError("Audio sender not found in RTCPeerConnection.")

    def get_stats(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.pc.getStats())

    def get_info(self):
        return {
            "chat_guid": self.chat_guid,
            "voice_chat_id": self.voice_chat_id,
            "connection_state": self.pc.connectionState,
            "ice_state": self.pc.iceConnectionState,
        }


class VoiceChatPlayer:
    logger = logging.getLogger("VoiceChatPlayer")

    async def heartbeat(self: "rubpy.Client", chat_guid: str, voice_chat_id: str) -> None:
        while True:
            try:
                await self.get_group_voice_chat_updates(chat_guid, voice_chat_id, int(time.time()))
                self.logger.debug(f"[Heartbeat] Updated for {chat_guid} / {voice_chat_id}")
                await asyncio.sleep(10)
            except (rubpy.exceptions.InvalidAuth, rubpy.exceptions.InvalidInput):
                self.logger.warning("[Heartbeat] Authentication/Input error, stopping heartbeat.")
                break
            except asyncio.CancelledError:
                self.logger.info("[Heartbeat] Cancelled.")
                break
            except Exception as e:
                self.logger.error(f"[Heartbeat] Unexpected error: {e}")
                await asyncio.sleep(5)

    async def speaking(self: "rubpy.Client", chat_guid: str, voice_chat_id: str) -> None:
        while True:
            try:
                await self.send_group_voice_chat_activity(chat_guid, voice_chat_id)
                self.logger.debug(f"[Speaking] Activity sent for {chat_guid}")
                await asyncio.sleep(1)
            except (rubpy.exceptions.InvalidAuth, rubpy.exceptions.InvalidInput):
                self.logger.warning("[Speaking] Authentication/Input error, stopping activity.")
                break
            except asyncio.CancelledError:
                self.logger.info("[Speaking] Cancelled.")
                break
            except Exception as e:
                self.logger.error(f"[Speaking] Unexpected error: {e}")
                await asyncio.sleep(2)

    async def voice_chat_player(
        self: "rubpy.Client",
        chat_guid: str,
        media: pathlib.Path
    ) -> VoiceChatConnection | None:
        if aiortc is None:
            self.logger.error("aiortc is not available.")
            return None

        class AudioFileTrack(MediaStreamTrack):
            kind = "audio"

            def __init__(self, player):
                super().__init__()  # MediaStreamTrack initializer
                self.player = player
                self._paused = False

            async def recv(self):
                while self._paused:
                    await asyncio.sleep(0.1)
                return await self.player.audio.recv()

            def pause(self):
                self._paused = True

            def resume(self):
                self._paused = False

        # Voice Chat ID detection
        chat_info = await self.get_info(chat_guid)
        voice_chat_id = chat_info.chat.find_keys('group_voice_chat_id')

        if voice_chat_id is None:
            voice_chat = (
                await self.create_group_voice_chat(chat_guid)
                # if chat_guid.startswith('g0') else
                # await self.create_channel_voice_chat(chat_guid)
            )
            voice_chat_id = voice_chat.find_keys('voice_chat_id') or (
                voice_chat.group_voice_chat_update.voice_chat_id if chat_guid.startswith('g0')
                else voice_chat.channel_voice_chat_update.voice_chat_id
            )

        self.logger.info(f"[VoiceChat] Starting voice chat in {chat_guid} with ID {voice_chat_id}")

        pc = RTCPeerConnection()
        media_player = MediaPlayer(str(media), decode=True)
        track = AudioFileTrack(media_player)
        pc.addTrack(track)

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        connect = await self.join_voice_chat(chat_guid, voice_chat_id, offer.sdp)
        sdp_answer = connect.sdp_answer_data

        await self.set_voice_chat_state(chat_guid, voice_chat_id)

        # Run activity tasks
        self._speaking_task = asyncio.create_task(self.speaking(chat_guid, voice_chat_id))
        self._heartbeat_task = asyncio.create_task(self.heartbeat(chat_guid, voice_chat_id))

        # Set remote SDP
        await pc.setRemoteDescription(RTCSessionDescription(sdp_answer, "answer"))

        # Logging connection changes
        @pc.on("iceconnectionstatechange")
        def on_ice_change():
            self.logger.info(f"[ICE] State changed: {pc.iceConnectionState}")

        @pc.on("connectionstatechange")
        def on_conn_change():
            self.logger.info(f"[Connection] State changed: {pc.connectionState}")

        return VoiceChatConnection(
            peer_connection=pc,
            media_player=media_player,
            audio_track=track,
            chat_guid=chat_guid,
            voice_chat_id=voice_chat_id,
            client=self
        )
