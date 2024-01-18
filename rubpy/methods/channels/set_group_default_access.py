from typing import Union


class SetGroupDefaultAccess:
    async def set_group_default_access(
            self,
            group_guid: str,
            access_list: Union[str, list],
    ):
        if isinstance(access_list, str):
            access_list = [access_list]

        return await self.builder('setGroupDefaultAccess',
                                  input={
                                      'group_guid': group_guid,
                                      'access_list': access_list,
                                  })