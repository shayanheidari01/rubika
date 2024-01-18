from typing import Literal, Optional
from pydantic import BaseModel
from .button_selection import ButtonSelection
from .button_calendar import ButtonCalendar
from .button_number_picker import ButtonNumberPicker
from .button_string_picker import ButtonStringPicker
from .button_location import ButtonLocation
from .button_textbox import ButtonTextbox


class Button(BaseModel):
    id: str
    type: Literal['Simple', 'Selection', 'Calendar', 'NumberPicker', 'StringPicker', 'Location', 'Payment',
                  'CameraImage', 'CameraVideo', 'GalleryImage', 'GalleryVideo', 'File', 'Audio', 'RecordAudio',
                  'MyPhoneNumber', 'MyLocation', 'Textbox', 'Link', 'AskMyPhoneNumber', 'AskLocation', 'Barcode']
    button_text: str
    button_selection: Optional[ButtonSelection]
    button_calendar: Optional[ButtonCalendar]
    button_number_picker: Optional[ButtonNumberPicker]
    button_string_picker: Optional[ButtonStringPicker]
    button_location: Optional[ButtonLocation]
    button_textbox: Optional[ButtonTextbox]
    # button_link: Optional[Link]