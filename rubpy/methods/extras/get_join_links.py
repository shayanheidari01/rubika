import rubpy


class GetJoinLinks:
    async def get_join_links(self: "rubpy.Client", object_guid: str) -> dict:
        """
        دریافت لینک‌های پیوستن به یک گروه/کانال خاص بر اساس object_guid.

        Args:
            object_guid (str): شناسه گروه یا کانال

        Returns:
            dict: پاسخ API شامل لینک‌های پیوستن
        """
        return await self.builder('getJoinLinks', input={'object_guid': object_guid})
