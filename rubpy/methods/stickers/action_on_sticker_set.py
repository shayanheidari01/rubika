import rubpy

class ActionOnStickerSet:
    async def action_on_sticker_set(
            self: "rubpy.Client",
            sticker_set_id: str,
            action: str = 'Add',
    ):
        if action not in ('Add', 'Remove'):
            raise ValueError('The `action` argument can only be in `("Add", "Remove")`.')

        return await self.builder(name='actionOnStickerSet',
                                  input={
                                      'sticker_set_id': sticker_set_id,
                                      'action': action,
                                  })