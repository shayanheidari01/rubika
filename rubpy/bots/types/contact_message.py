from pydantic import BaseModel


class ContactMessage(BaseModel):
    phone_number: str
    first_name: str
    last_name: str