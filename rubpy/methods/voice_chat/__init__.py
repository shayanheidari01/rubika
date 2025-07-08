from .set_voice_chat_state import SetVoiceChatState
from .send_group_voice_chat_activity import SendGroupVoiceChatActivity
from .join_voice_chat import JoinVoiceChat

class VoiceCall(
    SetVoiceChatState,
    SendGroupVoiceChatActivity,
    JoinVoiceChat,
):
    pass