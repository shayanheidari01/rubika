from .get_my_sticker_sets import GetMyStickerSets
from .action_on_sticker_set import ActionOnStickerSet
from .get_sticker_set_by_id import GetStickerSetByID
from .get_stickers_by_emoji import GetStickersByEmoji
from .get_stickers_by_set_ids import GetStickersBySetIDs
from .get_trend_sticker_sets import GetTrendStickerSets
from .search_stickers import SearchStickers


class Stickers(
    GetMyStickerSets,
    ActionOnStickerSet,
    GetStickerSetByID,
    GetStickersByEmoji,
    GetStickersBySetIDs,
    GetTrendStickerSets,
    SearchStickers,
):
    pass