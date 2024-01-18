from typing import Union


class GetAbsObjects:
    async def get_abs_objects(
            self,
            object_guids: Union[str, list],
    ):
        if isinstance(object_guids, str):
            object_guids = list(object_guids)

        return await self.builder('getAbsObjects',
                                  input={
                                      'object_guids': object_guids,
                                  })