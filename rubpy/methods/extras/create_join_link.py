from typing import Optional, Dict, Any
import rubpy


class CreateJoinLink:
    async def create_join_link(
        self: "rubpy.Client",
        object_guid: str,
        expire_time: Optional[int] = None,
        request_needed: bool = False,
        title: Optional[str] = None,
        usage_limit: int = 0,
    ) -> Dict[str, Any]:
        """
        ساخت لینک دعوت برای گروه یا کانال.

        Args:
            object_guid (str): شناسه گروه یا کانال.
            expire_time (Optional[int]): زمان انقضا لینک به ثانیه (اختیاری).
            request_needed (bool): آیا پذیرش درخواست عضویت دستی باشد یا خیر.
            title (Optional[str]): عنوان لینک (اختیاری).
            usage_limit (int): محدودیت تعداد استفاده از لینک.

        Returns:
            dict: پاسخ API شامل لینک ایجاد شده.
        
        Raises:
            ValueError: اگر مقدار `request_needed` بولی نباشد.
        """
        if not isinstance(request_needed, bool):
            raise ValueError('`request_needed` must be of boolean type only')

        data = {
            "object_guid": object_guid,
            "request_needed": request_needed,
            "usage_limit": usage_limit,
        }

        if isinstance(expire_time, int):
            data["expire_time"] = expire_time

        if isinstance(title, str):
            data["title"] = title

        return await self.builder("createJoinLink", input=data)
