from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class File(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None
    file_name: Optional[str] = None
    cdn_tag: Optional[str] = None

class Sticker(BaseModel):
    emoji_character: Optional[str] = None
    w_h_ratio: Optional[str] = None
    sticker_id: Optional[str] = None
    file: Optional[File] = None
    sticker_set_id: Optional[str] = None

class SetImage(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None
    cdn_tag: Optional[str] = None

class TrendStickerSet(BaseModel):
    sticker_set_id: Optional[str] = None
    title: Optional[str] = None
    count_stickers: Optional[int] = None
    set_image: Optional[SetImage] = None
    top_stickers: Optional[List[Sticker]] = None
    share_string: Optional[HttpUrl] = None
    update_time: Optional[int] = None

class GetTrendStickerSets(BaseModel):
    sticker_sets: Optional[List[TrendStickerSet]] = None
    next_start_id: Optional[str] = None
    has_continue: Optional[bool] = None

class GetStickersBySetIDs(BaseModel):
    stickers: Optional[List[Sticker]] = []

class StickerSets(BaseModel):
    sticker_set_id: Optional[str] = None
    title: Optional[str] = None
    count_stickers: Optional[int] = None
    set_image: Optional[SetImage] = None
    top_stickers: Optional[List[Sticker]] = []

class GetMyStickerSets(BaseModel):
    sticker_sets: Optional[List[StickerSets]] = []