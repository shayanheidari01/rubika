class GetLinkFromAppUrl:
    async def get_link_from_app_url(
            self,
            app_url: str,
    ):
        return await self.builder('getLinkFromAppUrl',
                                  input={
                                      'app_url': app_url,
                                  })