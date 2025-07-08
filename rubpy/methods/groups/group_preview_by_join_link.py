import rubpy

class GroupPreviewByJoinLink:
    async def group_preview_by_join_link(
            self: "rubpy.Client",
            link: str,
    ) -> rubpy.types.Update:
        """
        Get group preview by join link.

        Args:
        - link (str): The join link or hash link.

        Returns:
        - rubpy.types.Update: Update object containing the group preview information.
        """
        if '/' in link:
            link = link.split('/')[-1]

        return await self.builder('groupPreviewByJoinLink',
                                  input={
                                      'hash_link': link,
                                  })
