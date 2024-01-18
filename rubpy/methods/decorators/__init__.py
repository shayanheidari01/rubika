from .on_message_updates import OnMessageUpdates
from .on_remove_notifications import OnRemoveNotifications
from .on_show_notifications import OnShowNotifications
from .on_chat_updates import OnChatUpdates
from .on_show_activities import OnShowActivities


class Decorators(
    OnMessageUpdates,
    OnChatUpdates,
    OnRemoveNotifications,
    OnShowActivities,
    OnShowNotifications,
):
    pass