from datetime import datetime
from pydantic import BaseModel


class Location(BaseModel):
    id: str
    company_id: str
    loc_name: str
    latitude: float
    longitude: float
    radius: float
    created_at: datetime
