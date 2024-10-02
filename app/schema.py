from pydantic import BaseModel
from typing import List, Optional

class RestaurantCreateRequest(BaseModel):
    name: str
    restaurant_user_id: int
    logo_svg: Optional[str] = None
    cover_photo_svg: Optional[str] = None
    branches: Optional[List[str]] = None
    primary_number: Optional[str] = None
    secondary_number: Optional[str] = None
