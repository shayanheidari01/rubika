import rubpy

class JoinGroup:
    async def join_group(
            self: "rubpy.Client",
            link: str,
    ) -> rubpy.types.Update:
        """
        Join a group using the provided link.

        Args:
        - link (str): The group link or hash link.

        Returns:
        - rubpy.types.Update: Update object confirming the group join action.
        """
        if '/' in link:
            link = link.split('/')[-1]

        return await self.builder('joinGroup',
                                  input={
                                      'hash_link': link,
                                  })
