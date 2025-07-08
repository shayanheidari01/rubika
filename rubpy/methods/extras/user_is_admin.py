import rubpy

class UserIsAdmin:
    async def user_is_admin(
            self: "rubpy.Client",
            object_guid: str,
            user_guid: str,
    ) -> bool:
        """
        Checks if a user is an admin in a group or channel.

        Args:
            object_guid (str): The GUID of the group or channel.
            user_guid (str): The GUID of the user.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        has_continue = True
        next_start_id = None

        while has_continue:
            result = await self.get_group_admin_members(object_guid, next_start_id) if object_guid.startswith('g0') else await self.get_channel_admin_members(object_guid, next_start_id)
            has_continue = result.has_continue
            next_start_id = result.next_start_id

            for user in result.in_chat_members:
                if user_guid == user.member_guid:
                    return True

        return False
