from pydantic import BaseModel

class Location(BaseModel):
    longitude: str
    latitude: str