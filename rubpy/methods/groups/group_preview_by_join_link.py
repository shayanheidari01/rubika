import rubpy

class GroupPreviewByJoinLink:
    async def group_preview_by_join_link(
            self: "rubpy.Client",
            link: str,
    ):
        if '/' in link:
            link = link.split('/')[-1]

        return await self.builder(
            name='groupPreviewByJoinLink',
            input={
                'hash_link': link
            }
        )
