import rubpy
from rubpy.types import Update

class GetLinkFromAppUrl:
    async def get_link_from_app_url(
            self: "rubpy.Client",
            app_url: str,
    ) -> Update:
        """
        Retrieves a link from an application URL.

        Args:
            app_url (str): The application URL.

        Returns:
            rubpy.types.Update: The link data.
        """
        return await self.builder('getLinkFromAppUrl',
                                  input={
                                      'app_url': app_url,
                                  })
