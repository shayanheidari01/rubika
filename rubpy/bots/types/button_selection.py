from pydantic import BaseModel
from typing import Literal, List
from .button_selection_item import ButtonSelectionItem


class ButtonSelection(BaseModel):
    selection_id: str
    search_type: Literal[None, 'Local', 'Api']
    get_type: Literal['Local', 'Api']
    items: List[ButtonSelectionItem]
    is_multi_selection: bool
    columns_count: str
    title: str