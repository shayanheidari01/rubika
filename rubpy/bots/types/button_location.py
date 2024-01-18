from typing import Literal
from pydantic import BaseModel
from .location import Location


class ButtonLocation(BaseModel):
    default_pointer_location: Location
    default_map_location: Location
    type: Literal['Picker', 'View']
    title: str
    location_image_url: str