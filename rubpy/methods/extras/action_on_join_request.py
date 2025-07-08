import rubpy
from typing import Literal, Dict, Any


class ActionOnJoinRequest:
    async def action_on_join_request(
        self: "rubpy.Client",
        object_guid: str,
        user_guid: str,
        action: Literal['Accept', 'Reject'] = 'Accept'
    ) -> Dict[str, Any]:
        """
        انجام عملیات بر روی درخواست عضویت (تأیید یا رد).

        Args:
            object_guid (str): شناسه گروه یا کانال.
            user_guid (str): شناسه کاربری درخواست‌دهنده.
            action (Literal['Accept', 'Reject']): عملیات مورد نظر (پیش‌فرض 'Accept').

        Returns:
            dict: پاسخ API پس از انجام عملیات.

        Raises:
            ValueError: اگر action غیرمجاز باشد.
        """
        if action not in {'Accept', 'Reject'}:
            raise ValueError('`action` must be either "Accept" or "Reject".')

        object_type = 'Group' if object_guid.startswith('g0') else 'Channel'

        data = {
            'object_guid': object_guid,
            'object_type': object_type,
            'user_guid': user_guid,
            'action': action,
        }

        return await self.builder('actionOnJoinRequest', input=data)
