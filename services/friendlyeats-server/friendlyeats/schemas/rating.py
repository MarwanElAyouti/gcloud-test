from typing import Optional

from pydantic import BaseModel


class Rating(BaseModel):
    rating: int
    text: str
    userId: str = "123456789"
    userName: Optional[str] = "Anonymous"
    timestamp: Optional[str] = None
