import rubpy


class GetGroupOnlineCount:
    async def get_group_online_count(self: "rubpy.Client", group_guid: str):
        return await self.builder('getGroupOnlineCount', input=dict(group_guid=group_guid))