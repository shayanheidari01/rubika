class GetUserInfo:
    async def get_user_info(
            self,
            user_guid: str=None,
    ):
        result = await self.builder(
            name='getUserInfo',
            input={} if user_guid is None else {'user_guid': user_guid},
            tmp_session=True if self.auth is None else False,
        )
        return result