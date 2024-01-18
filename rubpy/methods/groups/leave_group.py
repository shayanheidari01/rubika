import rubpy

class LeaveGroup:
    async def leave_group(
            self: "rubpy.Client",
            group_guid: str,
    ):
        return await self.builder('leaveGroup', input=dict(group_guid=group_guid))