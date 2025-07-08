import rubpy


class GetJoinRequests:
    async def get_join_requests(self: "rubpy.Client", object_guid: str) -> dict:
        """
        دریافت درخواست‌های عضویت در گروه یا کانال مشخص‌شده.

        Args:
            object_guid (str): شناسه‌ی گروه یا کانال

        Returns:
            dict: پاسخ API شامل درخواست‌های عضویت
        """
        return await self.builder('getJoinRequests', input={'object_guid': object_guid})
