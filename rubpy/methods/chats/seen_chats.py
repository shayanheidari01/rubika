import rubpy

class SeenChats:
    async def seen_chats(
            self: "rubpy.Client",
            seen_list: dict,
    ) -> rubpy.types.Update:
        """
        Marks multiple chats as seen.

        Args:
            seen_list (dict): A dictionary containing chat GUIDs and their last seen message IDs.

        Returns:
            rubpy.types.Update: The result of the operation.
        """
        return await self.builder('seenChats',
                                  input={
                                      'seen_list': seen_list,
                                  })
