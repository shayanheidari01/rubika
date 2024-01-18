class JoinGroup:
    async def join_group(
            self,
            link: str,
    ):
        if '/' in link:
            link = link.split('/')[-1]

        return await self.builder('joinGroup',
                                  input={
                                      'link': link,
                                  })